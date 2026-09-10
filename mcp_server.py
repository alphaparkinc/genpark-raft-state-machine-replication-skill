import sys
import json
from client import RaftNode

def main():
    raft = RaftNode(node_id=1, peers=[2, 3])
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        req = json.loads(line)
        method = req.get("method")
        params = req.get("params", {})
        if method == "vote":
            ok, term = raft.handle_request_vote(params.get("term"), params.get("candidate_id"), 0, 0)
            res = {"granted": ok, "term": term}
        elif method == "append":
            ok, term = raft.append_entries(params.get("term"), params.get("leader_id"), 0, 0, params.get("entries", []), params.get("leader_commit", 0))
            res = {"success": ok, "term": term}
        else:
            res = {"error": "unknown method"}
        sys.stdout.write(json.dumps({"id": req.get("id"), "result": res}) + "\n")
        sys.stdout.flush()

if __name__ == "__main__":
    main()
