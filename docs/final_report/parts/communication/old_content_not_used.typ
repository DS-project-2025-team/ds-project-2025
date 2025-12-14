_Nodes_ communicate with each other by means of order-preserving messages. There are 4 different message types:
+ bootstrap/node discovery message (for finding everybody before starting tasks)
+ internally initiated request (heartbeat/vote request/response/configuration change/task distribution)
+ client request (?)
+ any response

=== Blocking and non-blocking messages
Sending may be blocking or non-blocking.

Blocking messages:
- client request
- configuration change
- task distribution

Non-blocking:
- heartbeat
- vote request
- node discovery
- any response

Message sender is called _the source_ node, and the receiver is called _the target_ node. This attempts to keep roles clear when describing multi-way messaging.

== Message properties
Messaging is order-preserving, that is, messages arrive in the same order they were sent (added to the pending queue).

All messages include source id, sequence number, message type, and payload, if necessary. Source id & sequence number make message unique. Using reliable (=lossless) messaging platform (e.g. Kafka) makes re-sending same message unnecessary.

== Sending a message
Every message has a client, either external (human/external app) or internal. Regardless of the type of client, messages are sent by the following rules.

When a new message is created in the source, it is added to an order-preserving _pending message queue_. If it is the only item in the queue it is sent immediately. Non-blocking message is removed after being sent from the pending messages queue. Blocking messages are moved from pending to _sent message queue_ instead.

Non-blocking client returns immediately after adding the message to the pending message queue whereas blocking client waits until required minimum number of responses arrives.

Sending blocking messages _must not_ prevent concurrent handling of receiving messages. Message receiving is good to make event based.

== Responding to a message
When message arrives at target node, it reads source's id, message number, and the type of the message.
Then the target node processes the message, if necessary, creates a response message, and sends it to the source node.

The response includes target node's id, payload, if necessary, and the original message number, which makes it possible for the source to identify to which message the response relates.

== Receiving response
Blocking clients wait for responses from targets. Every time a response arrives a handler (thread) reads the source id, message number and the type of the message. A message with identical message id is searched from the sent messages queue, and if this is the first response to the message from this target, then save the target id and increase response counter by one.

If the response counter is high enough after the increment, then notify message's client so that it can return, and that the message can also be removed from the sent messages queue. Otherwise the client waits until enough responses have arrived.


The Leader node sends heartbeats and ensures that all nodes in the system are operational. If the Leader node crashes, the Followers will notice this by the lack of heartbeats. In this case, the Followers will start a vote for a new Leader.

Nodes execute their tasks based on consistent receipts (=list of tasks).

Task sets are then assigned evenly to cluster nodes, which execute them until
- they, or any other node finds the solution,
- all tasks are done
- Leader sends new init work message, including new tasks, changed configuration, etc.
