== Current state of the control plane
Now there is a skeleton code for creating a cluster based on static node information stored in a file. Nodes find each other and they send ping messages to each other. Message handler template is there.

== Next Steps in control plane implementation
- Add a clock which causes a message be periodically sent.
- Create ApplyLog message including sequence number, and potential data (without data it acts only as heartbeat message)
-- create bookkeeping for sent ApplyLog messages, separate for each node (reset timer etc.)
- Create handler function for ApplyLog, which responds to the sender
-- create bookkeeping for received messages from the Leader (reset timer etc.)
- Add necessary debug logging
- Create persistent log for a node. Log entries include at least term, log index, operation id+content

- think about code structure, prevent functions from growing huge etc.

In general, the first version uses the messaging but is limited to non-blocking heartbeat message and its response. Or just the sending part, and the receivers detect message type and print its name.

The big think at this point is that every incoming message raises an event, which is handled by any available thread but without blocking any other threads.

Next heartbeat response can be added if not done already.

Node discovery logic must be designed and documented. It is one of the rare phases where all nodes communicate with each other. Something may be copied from the ping skeleton. This can be implemented and tested in isolation: start nodes and make sure they soon see each other and move from INIT phase to state where they can start electing the Leader (yes, I would keep discovery and Leader election clearly separate, former must be done before the latter can start).

Next more message types can be implemented, queues etc.

=== Some implementation compromises
- Message handling can be naive in the beginning, for example, detect the type and print it. Real functionality can be added once basics are done.
- Message queues can be single memory slots which can be accesses only one client at the time. It means that queue logic can be added later and that messaging is serialized; sending client blocks until previous message is removed from both, pending and sent "queues".
- First version could support only bootstrap- and task distribution messages and responses.

#pagebreak()
