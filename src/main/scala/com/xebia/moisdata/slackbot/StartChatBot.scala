package com.xebia.moisdata.slackbot

import akka.actor.ActorSystem
import com.typesafe.config.ConfigFactory
import dispatch._
import org.slf4j.LoggerFactory
import play.api.libs.json.Json
import slack.rtm.SlackRtmClient
import slack.{SlackUtil, models}

import scala.concurrent.ExecutionContextExecutor

object StartChatBot extends App {

  lazy val log = LoggerFactory.getLogger(getClass)

  lazy val pythonHostTfidf = url("http://127.0.0.1:5000/tfidf")
  lazy val pythonHostRNN = url("http://127.0.0.1:5000/rnn")

  val configFactory = ConfigFactory.load()
  val TOKEN = configFactory.getString("api.key")

  log.info(s"TOKEN: $TOKEN")

  implicit val system = ActorSystem("slack")
  implicit val ec: ExecutionContextExecutor = system.dispatcher

  val client = SlackRtmClient(TOKEN)
  val selfId: String = client.state.self.id

  client.onMessage { slackMessage =>
    val mentionedIds = SlackUtil.extractMentionedIds(slackMessage.text)

    if(mentionedIds.contains(selfId)) {

      var pythonHost = pythonHostRNN
      if(slackMessage.text.contains("!tf")) pythonHost = pythonHostTfidf

      val messageJson = generateContextAndMessage(slackMessage).toJson

      log.info(s"performing request to ${pythonHost.toRequest.getUrl} with JSON body ${Json.stringify(messageJson)}")
      val request = Http(pythonHost
        .addHeader("Content-Type", "application/json")
        .setBodyEncoding("UTF-8")
        .setBody(Json.stringify(messageJson))
        .POST
      )

      while (!request.isCompleted) {
        client.indicateTyping(slackMessage.channel)
        Thread.sleep(5000)
        log.info("thread sleeped")
      }

      request.map { response =>
        val cleanedAnswer = cleanAnswer(response.getResponseBody)

        log.debug(s"chatbot answering on ${slackMessage.channel} : $cleanedAnswer")
        client.sendMessage(slackMessage.channel, s"<@${slackMessage.user}> ".concat(cleanedAnswer))
      }
    }
  }

  private def cleanAnswer(response: String) = {
    response.replace("__eou__", "").replace("__eot__", "")
  }

  private def generateContextAndMessage(slackMessage: models.Message): Message = {
    val question = slackMessage.text.replace(s"<@$selfId>", "").replace("!tf", "")
    Contexts.add(slackMessage.user, question)
    val context = Contexts.toContext(slackMessage.user).getOrElse(question)
    Message(context, question)
  }
}
