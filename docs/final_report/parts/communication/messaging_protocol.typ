== Messaging Protocol

The system relies on reliable message passing to distribute work, maintain state, and detect failures. Messages are divided into two categories: external (user $<->$ system) and internal (node $<->$ node).

External Messages:
- INPUT — sent by user to submit formulas  
- OUTPUT — sent by Leader after computation

Internal Messages:

#table(
  columns: (auto, auto, auto, auto),
  align: horizon,
  table.header([*Purpose*],[*Message*], [*Direction*],[*Description*]),
  [Work distribution], [ASSIGN], [Leader $->$ Follower], [Assign a task and state hash],
  [Task reporting], [REPORT], [Follower $->$ Leader], [Report task result and state hash],
  [Acknowledgment], [OK], [Follower $->$ Leader], [Confirm receipt of ASSIGN message],
  [Outdated node updates itself], [GET_ENTRIES], [New Node $->$ Leader], [New or failed node joins the cluster],
  [Logging and failure detection], [APPEND_ENTRY], [Leader $->$ Follower], [Update replicated log/state, empty message for liveness check],
  [Acknowledgement], [APPENDENTRY \_RESPONSE], [Follower $->$ Leader], [Confirm receipt of an empty APPEND_ENTRY message],
)

== Message Flow Example:

- Leader sends ASSIGN $->$ Follower updates hash and computes.
- Follower sends REPORT $->$ Leader verifies hash and marks task complete.
- Leader optionally sends APPEND_ENTRY $->$ Follower proceeds with next task.

== Blocking vs Non-blocking Messages:

- Blocking: ASSIGN, INPUT, configuration changes $->$ sender waits for response.
- Non-blocking: APPEND_ENTRY, REPORT $->$ sender continues without waiting.

== Safety Measures:

- Sequence numbers and source IDs ensure unique and ordered messages.
- Hashes prevent outdated REPORT messages from corrupting state.
- At-most-once delivery (Kafka) ensures tasks are not redundantly executed.