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
Most of the functionalities are in the modules `raft` and `network` which we will discuss next.

#figure(
  include "/docs/final_report/images/prototype_architecture.typ",
  caption: [Prototype architecture],
)<fig:prototype_architecture>

The module `raft` contains all functionalities related to Raft algorithm, including the node states (roles) and classes for log and log entries.

Following single responsibility principle, the messaging functionalities of Leader and Follower are extracted into corresponding `Messager` classes.
This is not done for Candidate due to lack of time.

The module `network` encapsulates the producer (for sending) and consumer (for receiving) provided by aiokafka.
Additionally, the construction of consumers for different topics is done using factory pattern.
Other modules only need to instantiate a producer for sending messages and one consumer per topic to receive messages.

Additionally, there could be separate classes for the payload of each message type.
Again, due to lack of time, this is only implemented for the most complex APPEND_ENTRIES message.

The payload of messages is serialized and deserialized using as JSON.
Implementing serialization and deserialization for each message is also possible but tedious, unlike using `derive` macros from `serde` library in Rust.
Therefore we did not choose that approach.
Additionally, the aiokafka library provides no types for message payload which causes potential type errors independent of how we implemented the serialization and deserialization.

== Starting

Next, we explain what our program does when it is started, see `README.md` for instructions of starting the system.

The entry point of a the program running a node is `main.py`, in which a `Node` instance is initialized and ran.
The `Node` runs the state machine in @fig:node_states in an infinite loop.

Each time running a role, a new instance of that role is created and ran.
The role changes when the previous role ends and return the next role.
Each role gets the log object when initialized and they update it according to Raft algorithm~@ongaro_2014_raft.

The nodes run several event loops concurrently for polling messages.
Whenever a message arrives, the node processes it, sends responses if needed and then continues waiting.
For example, a Follower works as follows:
+ Poll ASSIGN messages
  + When a message arrives, compute satisfiability for the assigned interval.
  + Send a REPORT message.
+ Poll APPEND_ENTRIES messages
  + Update log and respond to APPEND_ENTRIES messages with APPENDENTRY_RESPONSE message
Additionally, some common functionalities, such as voting and responding to PING messages are handled in `Node` class itself.

Lastly, we have tested the prototype with 3, 4 and 5 nodes.
The Leader election worked fine with all test configurations.
The situation where the Leader dies was tested with different configurations.
That worked well and new Leader was selected in all cases.
We also tested how our prototype solves the given SAT-problem.
It also worked with different inputs.
