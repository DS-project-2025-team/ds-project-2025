= Introduction

This report presents the design and architecture of a distributed brute‑force 3‑SAT solver implemented with Python and Kafka message broker.

The system evaluates Boolean formulas in 3‑Conjunctive Normal Form (3‑SAT), such as~$(x_1 or x_2 or x_3) and (not x_2 or not x_3 or x_4)$, and determines whether there exists an assignment of Boolean values that satisfies the formula.

Because the search space grows exponentially with the number of variables, brute‑force evaluation is computationally expensive.
To address this, we distribute the work across up to thousands of identical nodes using a Leader–Follower architecture.
The Leader partitions the search space into independent intervals and assigns computation tasks to Followers, which evaluate them in parallel.

Fault tolerance is achieved through task redundancy, and Raft consensus algorithm~@ongaro_2014_raft for Leader election and Leader state replication.
Followers can join and leave dynamically, and the system tolerates node failures by reassigning tasks and potentially electing a new Leader.
The goal is a robust, scalable distributed computation system capable of solving large 3‑SAT instances correctly while maintaining shared state, ensuring consistency, and tolerating node failures.

This report is organized as follows: @sect:background introduces 3-SAT problem, @sect:architecture describes the architecture.
