== Messaging Protocol

The system relies on a message broker to distribute work, maintain state, and detect failures.
Messages are divided into two categories: external (User $<->$ System) and internal (Node $<->$ Node).

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

Additionally, the freshness of messages are identified by hashes, content, sender IDs etc.
For example outdated REPORT messages can be detected by hashes of formulas and outdated VOTE_REQUEST can be detected by term.
Therefore message ordering is not required.

However, we require at-least-once delivery for blocking messages, their responses and REPORT messages.
Only ASSIGN messages require at-most-once delivery.
