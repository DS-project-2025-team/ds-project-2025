== Initialization

In _Initialization_ state, all nodes start as Follower and connect to the message broker.
At this point there are no APPEND_ENTRIES messages in the system.
This indicates that there is no Leader in the system.
Because of that the system enters the _Leader election_ state.
The election is done using Raft algorithm with random UUIDs as node IDs.
There are $2^122$ different random UUIDs~@uuid_rfc9562, hence the possibility of duplicate UUIDs is negligible.

After Leader election, the system enters Ready state.
