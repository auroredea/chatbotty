package com.xebia.moisdata.slackbot

import play.api.libs.json.{JsValue, Json, Reads, Writes}


case class Message(context: String, question: String) {
  def toJson: JsValue = Json.toJson(this)
}

object Message {
  implicit val writes: Writes[Message] = Json.writes[Message]
  implicit val reads: Reads[Message] = Json.reads[Message]
}