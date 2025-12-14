== Initialization

In _Initialization_ state, all nodes start as Follower and connect to the message broker.
At this point there are no APPEND_ENTRIES messages in the system.
This indicates that there is no Leader in the system.
Some Follower will eventually detect that using election timeout and became a Canditate.

The Candidate will first send a PING message to all nodes.
The number of replies is used as the number of nodes.
This is needed because initially nodes does not know each other.

After that the Candidate will send VOTE_REQUEST messages to all nodes and the system enters the _Leader election_ state.
When some Candidate wins the election, the system enters Ready state.

If some PING responses are lost, the Candidates might not agree on the number of nodes and the system might get multiple Leaders.
In this case, the Leaders will detect each other and revert back to Followers, see @ongaro_2014_raft.
The same election process is repeated until there is exactly one Leader.
