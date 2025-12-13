= Fault tolerance

Faults may occur in both, compute and control plane.

== Fault tolerance in the Compute Plane

The fault tolerance of the system is based on the principle that recomputing does not change the result, only uncompleted tasks can affect the result.

Previously, we introduced a hash for each ASSIGN message indicating the state of a Follower.
The Follower updates its hash immediately after receiving the ASSIGN message but the leader updates only after receiving the reply.
This can lead to different hashes in case of message loss or messages arriving in different order.
Next, we show that this does not matter.

When the Leader receives a REPORT message from a Follower, the only cases are that the hashes of Leader and Follower differ or are the same.

If the hashes are the same, then the result is valid and the Leader can reset the hash to ignore duplicates.

If the hashes are different, the Leader ignores the message.
If it is caused by messages arriving in different order, then the message is outdated and it does not matter.

Next, we consider the case where some messages are lost and hashes differ.

We note that the Follower node always have hash of its latest state, since it updates it first.
Additionally, the Leader only updates Follower hash after receiving OK.
In this case, the Follower has received the new task but the Leader did not receive OK message.
Then the Leader will assign the task again, possibly to other nodes.
If the Follower sends a REPORT with the old hash, then it will be ignored.

We assume that the REPORT marks all assigned tasks done.
If the Leader successfully assigns different tasks after a lost OK message of ASSIGN, then the REPORT message of the Follower will mark all successful and failed assignments at once.
Although, the Leader only knows the successful assignments.
Particularly, no tasks are not done.

== Fault tolerance in the Control Plane

The cluster runs Raft consensus algorithm. The number of members can be anything between 2 to thousands. A cluster with _2n+1_ members tolerates _n_ (fail-stop) faults.

Configuration changes may be started internally, when a node fails, or is restarted, for example, or externally, when a new node joins the cluster.

Nodes communicate with messages which are sent to and received from a Kafka cluster. The properties of Kafka guarantee similar safety properties as Raft, _2n+1_ Kafka instances tolerate _n_ faults.

