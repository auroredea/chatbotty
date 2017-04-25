name := """chatbotty"""

version := "1.0"

scalaVersion := "2.11.8"

// Change this to another test framework if you prefer
libraryDependencies += "org.scalatest" %% "scalatest" % "2.2.4" % "test"

// Uncomment to use Akka
//libraryDependencies += "com.typesafe.akka" %% "akka-actor" % "2.4.14"
libraryDependencies += "com.typesafe.akka" %% "akka-slf4j" % "2.4.14"

// Slack API
libraryDependencies += "com.github.gilbertw1" %% "slack-scala-client" % "0.2.1"

//Logging
libraryDependencies ++= Seq("org.slf4j" % "slf4j-api" % "1.7.25",
                            "org.slf4j" % "slf4j-simple" % "1.7.25")

libraryDependencies += "net.databinder.dispatch" %% "dispatch-core" % "0.11.2"

//fork in run := true