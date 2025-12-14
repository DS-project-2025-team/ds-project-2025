== Messaging Protocol

The system relies on a message broker to distribute work, maintain state, and detect failures.
Messages are divided into two categories: external (user $<->$ system) and internal (node $<->$ node).

#figure(
  table(
    columns: (auto, auto, auto),
    align: (left, left, left),

    table.header([*Message*], [*Direction*], [*Purpose*]),
    [INPUT], [User $->$ Leader], [User input],
    [OUTPUT], [Leader $->$ User], [Outputting result],

    [PING], [Candidate $->$ Node], [Detecting other nodes],

    [VOTE_REQUEST], [Candidate $->$ Node], [Leader election],

    [ASSIGN], [Leader $->$ Follower], [Work distribution],

    [REPORT], [Follower $->$ Leader], [Task reporting],

    [GET_ENTRIES], [Follower $->$ Leader], [Updating outdated nodes],

    [APPEND_ENTRIES], [Leader $->$ Follower], [Logging and failure detection],
  ),
  caption: [Purposes of different message types],
)<table:message_types>


The message types are shown in @table:message_types.
The messages VOTE_REQUEST, PING, APPEND_ENTRIES and GET_ENTRIES have corresponding acknowledgement messages.
These and INPUT are blocking messages, the sender does not send same message type before receiving responses or timeout.
The messages ASSIGN and REPORT are non-blocking, the sender can send multiple messages of these type without waiting.

Since the messaging is done in asynchronous functions, the sender can execute other asynchronous functions while waiting for response.
The blocking only means whether the sender waits for responses before sending messages of same type.

== Safety Measures:

- Sequence numbers and source IDs ensure unique and ordered messages.
- Hashes prevent outdated REPORT messages from corrupting state.
- At-most-once delivery (Kafka) ensures tasks are not redundantly executed.
