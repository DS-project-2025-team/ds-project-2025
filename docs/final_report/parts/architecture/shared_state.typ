== Shared state

Shared state is maintained by the Leader and replicated to Followers.
The state includes
- cluster membership information (nodes)
- uncompleted tasks
- user inputs (3-SAT formulas)

From these we note that the shared state changes, for example when
- a node joins or leaves the system
- a task is reported
- a user submits an input
- the computation of an input is completed
- the Leader changes

For consistent state replication, the system uses _log_ following Raft~@ongaro_2014_raft architecture.
Each change of the state is represented by a _log entry_ which is replicated to all nodes.
Only the Leader can add new entries to log and decide when to _commit_ (apply) them.

When the Leader wants to change the state, it appends an entry to its log and send the entry to all Followers.
When a Follower receives an entry, it checks whether the entry is valid and sends an acknowledgement to the Leader, see~@ongaro_2014_raft.
The acknowledgement contains whether the check is successful and other information for Raft.

After the Leader receives successful acknowledgements from the majority of the nodes, it commits the entry.
Next time when the Leader appends new entries, it sends the highest index of the committed entries and all Followers with valid log will commit all entries up to the index.
