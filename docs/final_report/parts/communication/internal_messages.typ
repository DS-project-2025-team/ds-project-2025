== Internal messages

In _Initialization_ state, all nodes read a pre-configured file of the IP addresses and ports of all nodes.
All the nodes start in the Follower state.
At this point there are no APPEND_ENTRY messages in the system.
This indicates that there is no Leader in the system.
Because of that the system enters the _Leader election_ state.
The election is done using Raft algorithm with IP address and port as node ID.
The combination of IP address and port can be represented a unique binary number.

After Leader election, the system enters Ready state.
In this state, the Leader takes user inputs and distributes the work among Follower nodes using ASSIGN messages.
The ASSIGN message contains a task and a hash indicating the Follower state.
When the Follower receives the ASSIGN message it updates its hash and replies with an OK message.

When a Follower completes its calculation, it sends a REPORT message with the results.
The REPORT includes the hash and a node ID and a boolean indicating satisfiability.
When the Leader receives the REPORT message, it compares the hash with current one.
If the hash does not match, then the message is outdated and the Leader ignores it.

Next, we will discuss the messages related to failures.
Currently, we have identified two error states: _Leader failure_ and _Follower failure_.

The failure handling is based on the principle that recomputing does not change the result, only uncompleted tasks can affect the result.
Particularly, a satisfiable assignment can appear in any subinterval.
Thus, in case of failure, recomputing is always a valid solution.

For detecting both Leader and Follower failures, we use APPEND_ENTRY messages.
The Leader sends periodically an empty APPEND_ENTRY to all Followers which must respond with an APPENDENTRY_REPONSE message.
If a Follower does not receive a APPEND_ENTRY message within a certain time window, it converts it self to CANDIDATE, increases the term, and initiates a Leader election.
If a Follower does not respond within a certain time window, then the Leader writes "node fail" log record, (eventually) runs it and redistributes its tasks and sets its hash to a new value.

Lastly, when a new node joins the system, it sends a GET_ENTRIES message to the Leader, which writes "node join" log record, (eventually) changes the cluster configuration. The log is replicated to the new node as well, and new node becomes a cluster member (FOLLOWER) as soon as it receives and writes the replicated log record to its own log.
