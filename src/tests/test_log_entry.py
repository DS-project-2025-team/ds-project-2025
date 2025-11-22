from entities.log_entry import LogEntry


def test_log_entry_init():
    cmd = {"type": "NODE_JOIN", "node_id": "node1"}
    entry = LogEntry(term=1, command=cmd)

    assert entry.term == 1
    assert entry.command == cmd
