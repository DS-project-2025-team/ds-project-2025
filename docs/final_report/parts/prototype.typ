= Prototype

We implemented a prototype of the system using Python, Kafka and aiokafka library.
The project source is available at https://github.com/DS-project-2025-team/ds-project-2025.

Our prototype implements the following features:

- A simple script for user input.
  Modify the formula in `start_client()` in `tasks.py` to change input.

- Distributed computation of subintervals in different Follower nodes.

- Parallel computation of different subintervals in multiple processes within a Follower.

- Shared distributed state:
  Implemented using an ad hoc broadcast-based solution.

  The log and leader state are replicated to all nodes.
  The whole log and state is repeatedly copied to Followers without further validation.

- Synchronization and consistency:
  Partially implemented.

  The Leader maintains its state including uncompleted tasks and a queue of user inputs.
  The Leader repeatedly sends logs to all Followers with APPEND_ENTRIES message.
  Each message contains the whole log and state.

  Consistency is not implemented.

- Consensus: Implemented in Leader election.

- Fault tolerance: Follower failures are handled by design.
  Leader failure causes a Leader election and new Leader will be elected.
  However, user inputs might be lost due to lack of consistency.

  No incorrect results will be returned in any failure.
  REPORT and OUTPUT messages can be checked by the formula it contains.

- Scalability: New nodes can join the system while it is running.
  Kafka used in the system is also distributed message broker which can be scaled up.

== Structure

The high-level architecture of the prototype is shown in @fig:prototype_architecture.

#figure(
  include "/docs/final_report/images/prototype_architecture.typ",
  caption: [Prototype architecture],
)<fig:prototype_architecture>

== Starting

Next, we introduce how our program is started.
The entry point of a the program running a node is `main.py`, in which a `Node` instance is initialized and ran.
The `Node` runs the state machine in @fig:node_states in an infinite loop.


Followers run an event loop that:
1. Listens for ASSIGN messages
2. Computes satisfiability for the assigned interval
3. Sends REPORT messages
4. Responds to APPEND_ENTRIES messages with APPENDENTRY_RESPONSE message
5. Accepts new tasks until Leader signals completion

The prototype was tested with 3, 4, and 5 nodes. The Leader election worked fine with all test configurations. The situation where the Leader dies was tested with different configurations. That worked well and new Leader was selected in all cases. We also tested how our prototype solves the given SAT-problem. It also worked well with different configuration.
