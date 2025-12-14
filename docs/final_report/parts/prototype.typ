= Prototype

The implementation is written in Python using the following key components:
- Kafka — message broker
- asyncio — concurrency management for Followers
- Python bitwise operations — efficient SAT evaluation
- A Raft election mechanism — achieve consensus among nodes
- A Raft state replication mechanism — periodic state broadcasts

Followers run an event loop that:
1. Listens for ASSIGN messages
2. Computes satisfiability for the assigned interval
3. Sends REPORT messages
4. Responds to APPEND_ENTRIES messages with APPENDENTRY_RESPONSE message
5. Accepts new tasks until Leader signals completion

A prototype was tested with 3, 4, and 5 nodes. The Leader election worked fine with all test configurations. The situation where the Leader dies was tested with different configurations. That worked well and new Leader was selected in all cases. We also tested how our prototype solves the given SAT-problem. It also worked well with different configuration.
