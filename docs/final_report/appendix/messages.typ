== Messages

- Removed JOIN messages, the mechanism for Follower failure also covers the case of new node joining.

- Removed STATE message, APPEND_ENTRIES serves same purpose.

- Replaced HEARTBEAT with empty APPEND_ENTRIES as in Raft algorithm~@ongaro_2014_raft
