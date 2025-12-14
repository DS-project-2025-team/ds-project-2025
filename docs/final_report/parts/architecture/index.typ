= Architecture<sect:architecture>

The distributed brute-force 3-SAT solver runs on top of a multi-node cluster following Raft architecture~@ongaro_2014_raft, consisting of one _Leader_ and multiple _Follower_ nodes, shown in @fig:roles.
The Leader distributes the computation in small batches to nodes, which compute the tasks independently.

For messaging, the system uses a message broker based on _producer-consumer_ model and topics.
In the model, the message senders are called _producers_ and receivers are _consumers_.
Producers send messages to the message broker.
Messages are categorized by topics and consumers poll messages by topic from the message broker.

In this section, we first introduce the workflow inside the system, from user submitting input to receiving output.
Next, we discuss the states of the nodes in the system.
Lastly, we discuss shared state in the system and its replication.

#figure(
  include "/docs/final_report/images/roles.typ",
  caption: [Leader $L$ and Followers $F_1,...,F_n$.],
)<fig:roles>

#include "workflow.typ"
#include "node_states.typ"
#include "shared_state.typ"
