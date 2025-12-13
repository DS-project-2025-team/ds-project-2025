== Messages

- Replaced JOIN message with GET_ENTRIES so that node failure and new node joining can be handled with same message.

- Removed STATE message, APPEND_ENTRIES serves same purpose.

- Replaced HEARTBEAT with empty APPEND_ENTRIES as in Raft algorithm.