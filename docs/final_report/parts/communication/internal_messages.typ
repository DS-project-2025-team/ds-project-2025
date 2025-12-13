== Internal messages

In _Initialization_ state, all nodes start as Follower and connect to the message broker.
At this point there are no APPEND_ENTRIES messages in the system.
This indicates that there is no Leader in the system.
Because of that the system enters the _Leader election_ state.
The election is done using Raft algorithm with random UUIDs as node IDs.
There are $2^122$ different random UUIDs~@uuid_rfc9562, hence the possibility of duplicate UUIDs is negligible.

After Leader election, the system enters Ready state.
In this state, the Leader takes user inputs and distributes the work to Followers using ASSIGN messages.
The ASSIGN message contains a SAT formula and a subinterval.

When the Follower receives the ASSIGN message it does the computation and sends a REPORT message with the results.
The REPORT includes a formula itself and its hash, subinterval and boolean indicating satisfiability.

When the Leader receives the REPORT message, it compares the hash with the hash of the current formula.
If the hashes match and then compares the formula itself.
If the something does not match, then the message is outdated and the Leader ignores it.

Next, we will discuss the messages related to failures.
Currently, we have identified two error states: _Leader failure_ and _Follower failure_.

The failure handling is based on the principle that recomputing does not change the result, only uncompleted tasks can affect the result.
Particularly, a satisfiable assignment can appear in any subinterval.
Thus, in case of failure, recomputing is always a valid solution.

For detecting both Leader and Follower failures, we use APPEND_ENTRIES messages.
The Leader sends periodically an empty APPEND_ENTRIES to all Followers which must respond with an APPENDENTRY_REPONSE message.
If a Follower does not receive a APPEND_ENTRIES message within a certain time window, it converts it self to CANDIDATE, increases the term, and initiates a Leader election.
If a Follower does not respond within a certain time window, then the Leader appends a "node fail" log entry.

Lastly, when a new node joins the system, it sets itself to Follower and sends a GET_ENTRIES message to the Leader, see @fig:new_node_joining.
When the Leader receives the message, it detects a new node and appends "node join" log entry and (eventually) changes the cluster configuration.
The entry is replicated to the new node as well.

#figure(
  include "/docs/final_report/images/new_node_joining.typ",
  caption: [A new node $N$ joins to the system],
)<fig:new_node_joining>