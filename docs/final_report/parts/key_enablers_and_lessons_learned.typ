= Key enablers and lessons learned<sect:key_enablers_and_lessons_learned>

The most important lesson we learned during development was that Python was a bad choice for our prototype and generally for larger projects.
Rust might be a better choice, although some of us have not written Rust.

The greatest weakness of Python is dynamic typing.
The aiokafka library we used did not have precise types for message objects.
This caused many serialization and type errors in runtime.

Additionally, Python does not provide `Mutex` wrappers like in Rust.
This makes it easy to forget locks and cause race conditions that are difficult to debug.
Also, the exception-based error handling did not work well.
Exceptions are often unexpected and not catched.
Rust-like `Result` enum would be better.

Next lesson we learned was not to log everything into INFO level.
This flooded the logs with mostly useless lines about sending and receiving messages.
Therefore, we moved sending and receiving of individual messages to DEBUG level.

Lastly, we underestimated the difficulty of the project and overestimated available time.
Hence not all planned features were implemented.

Additionally, we noted the following key enablers during development.

- Logging, it is almost impossible to debug the communication between nodes without logging.

- Asynchronous programming experience, the prototype would have even less features without it.

- The clear cheatsheet in Raft article @ongaro_2014_raft[Figure 2].
  This saved us a lot of time.

- Message broker (Kafka), without it we would have to maintain the information of other nodes in each node and implement node discovery.

- Colored log output, it is hard to find important lines (ERROR, WARNING) without colors since most lines are INFO level.
