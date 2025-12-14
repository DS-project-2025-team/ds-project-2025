== Messaging Protocol

The system relies on a message broker to distribute work, maintain state, and detect failures.
Messages are divided into two categories: external (user $<->$ system) and internal (node $<->$ node).

The message types are shown in @table:message_types.
The messages VOTE_REQUEST, APPEND_ENTRIES and GET_ENTRIES have corresponding acknowledgement messages.

#figure(
  table(
    columns: (auto, auto, auto),
    align: (left, left, left),

    table.header([*Message*], [*Direction*], [*Purpose*]),
    [INPUT], [User $->$ Leader], [User input],
    [OUTPUT], [Leader $->$ User], [Outputting result],

    [VOTE_REQUEST], [Candidate $->$ Node], [Leader election],

    [ASSIGN], [Leader $->$ Follower], [Work distribution],

    [REPORT], [Follower $->$ Leader], [Task reporting],

    [GET_ENTRIES], [Follower $->$ Leader], [Updating outdated nodes],

    [APPEND_ENTRIES], [Leader $->$ Follower], [Logging and failure detection],
  ),
  caption: [Purposes of different message types],
)<table:message_types>


== Message Flow Example:

- Leader sends ASSIGN $->$ Follower updates hash and computes.
- Follower sends REPORT $->$ Leader verifies hash and marks task complete.
- Leader optionally sends APPEND_ENTRIES $->$ Follower proceeds with next task.

== Blocking vs Non-blocking Messages:

- Blocking: ASSIGN, INPUT, configuration changes $->$ sender waits for response.
- Non-blocking: APPEND_ENTRIES, REPORT $->$ sender continues without waiting.

== Safety Measures:

- Sequence numbers and source IDs ensure unique and ordered messages.
- Hashes prevent outdated REPORT messages from corrupting state.
- At-most-once delivery (Kafka) ensures tasks are not redundantly executed.
