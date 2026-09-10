from client import RaftNode

def main():
    print("=== Testing Raft State Machine Replication Engine ===")
    raft = RaftNode(node_id=1, peers=[2, 3])
    ok, term = raft.handle_request_vote(term=1, candidate_id=2, last_log_idx=0, last_log_term=0)
    print(f"Candidate vote response: {ok}, term: {term}")
    assert ok and term == 1

    ok2, _ = raft.append_entries(term=1, leader_id=2, prev_log_idx=0, prev_log_term=0, entries=[{"term": 1, "command": "SET X=10"}], leader_commit=1)
    print(f"Append entries result: {ok2}, log size: {len(raft.log)}")
    assert ok2
    assert len(raft.log) == 1
    print("=== All tests passed successfully! ===")

if __name__ == "__main__":
    main()
