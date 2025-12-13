#import "@preview/dashy-todo:0.1.3": todo
#show link: underline

= Conclusions and lessons learned

The project repo can be found in #link("https://github.com/DS-project-2025-team/ds-project-2025")[Github].

== Conclusions #todo[Tämä kirjoitettava]

- what features are implemented in prototype
- future improvements
- scalability limitations - Kafka limits, network latency

A distributed 3-SAT system generalizes to other real-world distributed workloads such as distributed search problems, distributed rendering, or MapReduce-like workloads.

== Key enablers and lessons learned

We learned the following lessons:

- Python was a bad choice.
  Rust might have been a better choice, although some of us have not written Rust.

  - Python is not statically typed.
    The aiokafka library we used did not have precise types for message objects.
    This caused many serialization and type errors in runtime.

  - Python does not provide `Mutex` wrappers like in Rust.
    This makes it easy to forget locks and cause race conditions that are difficult to debug.

  - Error handling with exceptions does not work well.
    Exceptions are often unexpected and not catched.
    Rust-like `Result` enum would be better.

- Avoid logging everything to INFO level.
  Move sending and receiving of individual messages to DEBUG level.

- We underestimated the difficulty of the project and overestimated available time.
  Not all features were implemented.

The following were key enablers during development:

- Logging, it is almost impossible to debug the communication between nodes without logging.

- Asynchronous programming experience, the prototype would have even less features without it.

- The clear cheatsheet in Raft article @ongaro_2014_raft[Figure 2].
  This saved us a lot of time.

- Message broker (Kafka), without it we would have to maintain the information of other nodes in each node and node discovery.

- Colored log output, it is hard to find important lines (ERROR, WARNING) without colors since most lines are INFO level.
