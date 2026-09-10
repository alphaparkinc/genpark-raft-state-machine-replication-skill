class RaftNode:
    """
    Raft Consensus Engine implementing leader election and log replication.
    """
    def __init__(self, node_id, peers):
        self.node_id = node_id
        self.peers = peers
        self.current_term = 0
        self.voted_for = None
        self.log = []
        self.commit_index = 0
        self.role = "FOLLOWER"

    def handle_request_vote(self, term, candidate_id, last_log_idx, last_log_term):
        if term > self.current_term:
            self.current_term = term
            self.role = "FOLLOWER"
            self.voted_for = None

        can_vote = (self.voted_for is None or self.voted_for == candidate_id) and (term == self.current_term)
        if can_vote:
            self.voted_for = candidate_id
            return True, self.current_term
        return False, self.current_term

    def append_entries(self, term, leader_id, prev_log_idx, prev_log_term, entries, leader_commit):
        if term < self.current_term:
            return False, self.current_term
        self.current_term = term
        self.role = "FOLLOWER"
        self.log.extend(entries)
        if leader_commit > self.commit_index:
            self.commit_index = min(leader_commit, len(self.log))
        return True, self.current_term
