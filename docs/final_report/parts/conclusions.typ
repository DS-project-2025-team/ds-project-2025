#import "@preview/dashy-todo:0.1.3": todo
#show link: underline

= Conclusions

In this report, we introduced a distributed system for computing the satisfiability of 3-SAT formulas.
The system allows distributing computation among multiple nodes and ensures that no failures can lead to an incorrect result.

We used Raft algorithm~@ongaro_2014_raft for Leader election and log replication.
On top of that we designed a fault tolerant work distribution algorithm that runs on Leader.

We also implemented a prototype featuring parallel computation, Leader election, Leader state replication and fault tolerance among others.
Additionally, we measured its performance and identified some bottlenecks such as Follower idling and slow startup time due to Kafka or aiokafka library.
On top of that, we proposed possible optimizations to speed up computation.

Our system also generalizes to other real-world distributed workloads such as distributed search problems, distributed rendering, or MapReduce-like workloads.
