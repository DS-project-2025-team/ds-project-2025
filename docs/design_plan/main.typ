= Disctibuting shared global state and maintaining consensus in distributed prototype project

Shared state is maintained by the Leader and replicated to Followers. Every change in the state requires that the majority of all nodes (incl. the Leader) store the change command before the Leader is allowed to run the update. This sounds like _Raft_ but there are alternatives like _viewstamped replication_ or _Paxos_. This is something we need to decide.

=== Shared state

- cluster membership information (nodes, their connect strings etc.)
- Workload (== undone + completed tasks, mapped with their responsible nodes)
- configuration parameters (timeouts, etc.)
These all can be included in a single object for simplicity.

=== Synchronization and consistency (this is a bit tricky but I'll try)
- nodes execute their tasks based on consistent receipts (=list of tasks)
- ?

=== Fault tolerance

Optional. Raft, for example, includes failure detection. If the period where tasks are distributed to nodes is called _init work (phase)_ , then failure (or node addition) means re-init work with changed configuration (nodes). This is doable but may not fit in the schedule.

=== Scalability & performance

Optional. The workload (SAT) scales well as the tasks can be predefined and there's no dependency between tasks. Therefore the amount of work is known in the beginning of execution and that is when the Leader divides it into set of independent tasks. Task sets are then assigned evenly to cluster nodes, which execute them until
- they, or any other node finds the solution, 
- all tasks are done
- Leader sends new init work message, including new tasks, changed configuration, etc. 

In other words, the more there are nodes the faster all tasks are done.