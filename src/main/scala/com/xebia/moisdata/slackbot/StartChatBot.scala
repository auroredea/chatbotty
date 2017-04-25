package com.xebia.moisdata.slackbot

import akka.actor.ActorSystem
import com.typesafe.config.ConfigFactory
import org.slf4j.LoggerFactory
import slack.SlackUtil
import slack.rtm.SlackRtmClient
import dispatch._
import play.api.libs.json.Json

import scala.concurrent.ExecutionContextExecutor

object StartChatBot extends App {

  lazy val log = LoggerFactory.getLogger(getClass)

  lazy val pythonHost = url("http://127.0.0.1:5000/nlp")

  val configFactory = ConfigFactory.load()
  val TOKEN = configFactory.getString("api.key")

  log.info(s"TOKEN: $TOKEN")

  implicit val system = ActorSystem("slack")
  implicit val ec: ExecutionContextExecutor = system.dispatcher

  val client = SlackRtmClient(TOKEN)
  val selfId: String = client.state.self.id

  client.onMessage { message =>
    val mentionedIds = SlackUtil.extractMentionedIds(message.text)

    if(mentionedIds.contains(selfId)) {

      val question = message.text.replace(s"<@$selfId>", "")
      Contexts.add(message.user, question)
      val context = Contexts.toContext(message.user).getOrElse(question)
      val messageJson = Message(context, question).toJson

      log.info(s"performing request to ${pythonHost.toRequest.getVirtualHost} with JSON body ${Json.stringify(messageJson)}")
      val request = Http(pythonHost
        .addHeader("Content-Type", "application/json")
        .setBodyEncoding("UTF-8")
        .setBody(Json.stringify(messageJson))
        .POST
      )

      request.map { response =>
        log.debug(s"chatbot answering on ${message.channel} : \"${response.getResponseBody}\"")
        client.sendMessage(message.channel, response.getResponseBody)
      }
    }
  }

}
