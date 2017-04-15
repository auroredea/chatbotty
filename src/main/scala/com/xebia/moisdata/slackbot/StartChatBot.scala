package com.xebia.moisdata.slackbot

import akka.actor.ActorSystem
import com.typesafe.config.ConfigFactory
import org.slf4j.LoggerFactory
import slack.SlackUtil
import slack.rtm.SlackRtmClient

import scala.concurrent.ExecutionContextExecutor

object StartChatBot extends App {

  lazy val log = LoggerFactory.getLogger(getClass)

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
      client.sendMessage(message.channel, s"Bonjour <@${message.user}> !")
    }
  }

}
