from entities.log_entry import LogEntry
from entities.raft_log import RaftLog


def test_raft_log_init():
    raft_log = RaftLog(node_id="node1")

    assert raft_log.node_id == "node1"
    assert raft_log.entries == []
    assert raft_log.commit_index == -1
    assert raft_log.term == 0
    assert raft_log.leader_id is None
    assert raft_log.nodes == {}
    assert raft_log.tasks == {}
    assert raft_log.uncompleted_tasks == set()
    assert raft_log.formula is None


def test_raft_log_commit_and_revert():
    raft_log = RaftLog(node_id="node1")

    # Add entries
    cmd1 = {"type": "NODE_JOIN", "node_id": "node2"}
    raft_log.entries.append(LogEntry(term=1, command=cmd1))

    cmd2 = {"type": "ASSIGN_TASK", "task_id": "task1", "node_id": "node2"}
    raft_log.entries.append(LogEntry(term=1, command=cmd2))

    # Commit first entry
    raft_log.commit()
    assert raft_log.commit_index == 0
    assert "node2" in raft_log.nodes

    # Commit second entry
    raft_log.commit()
    assert raft_log.commit_index == 1
    assert raft_log.tasks["task1"] == "node2"
    assert "task1" in raft_log.uncompleted_tasks

    # Revert to first entry
    raft_log.revert(0)
    assert len(raft_log.entries) == 1
    assert raft_log.commit_index == 0


def test_raft_log_apply_entry_node_fails():
    raft_log = RaftLog(node_id="node1")

    # Simulate node join
    raft_log.apply_entry({"type": "NODE_JOIN", "node_id": "node2"})
    assert raft_log.nodes["node2"]["status"] == "alive"

    # Assign task to node2
    assign_cmd = {"type": "ASSIGN_TASK", "task_id": "task1", "node_id": "node2"}
    raft_log.apply_entry(assign_cmd)
    assert raft_log.tasks["task1"] == "node2"
    assert "task1" in raft_log.uncompleted_tasks

    # Simulate node failure
    raft_log.apply_entry({"type": "NODE_FAILS", "node_id": "node2"})
    assert raft_log.nodes["node2"]["status"] == "failed"
    assert "task1" not in raft_log.tasks
    assert "task1" in raft_log.uncompleted_tasks
