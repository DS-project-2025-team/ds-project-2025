= Introduction

This report presents the design and architecture of a distributed brute-force 3-SAT solver implemented with Python and Kafka message broker.

The system evaluates Boolean formulas in 3-Conjunctive Normal Form (3-SAT), such as~$(x_1 or x_2 or x_3) and (not x_2 or not x_3 or x_4)$, and determines whether there exists an assignment of Boolean values that satisfies the formula.

Because the search space grows exponentially with the number of variables, brute-force evaluation is computationally expensive.
To address this, we distribute the work across up to thousands of identical nodes using a Leader–Follower architecture.
The Leader partitions the search space into independent intervals and assigns computation tasks to Followers, which evaluate them in parallel.

It is possible to modify the system to support other parallel computation tasks.
For example, the brute-force algorithm can be replaced with a more efficient algorithm.
Also, the system can be modified to support any computation that can be splitted into independent subtasks.

For our system, the most important requirement is the correctness of computation.
Particularly, no tasks should be skipped unless the formula is satisfiable.
To ensure this in failure cases, we allow sending redundant tasks and use Raft consensus algorithm~@ongaro_2014_raft for Leader state replication and Leader election.

On top of that, our goals include building a robust and scalable distributed computation system capable of solving large 3-SAT instances while maintaining shared state, consistency, and tolerating node failures.

This report is organized as follows: @sect:background introduces 3-SAT problem, @sect:architecture describes the architecture.
