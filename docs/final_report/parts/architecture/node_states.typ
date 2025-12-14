== Node states

Next, we discuss the node states.
Each node operate in one of three states: _Leader_, _Follower_ and _Candidate_.
The transitions between them are shown in @fig:node_states.

The Leader manages task assignment, shared state updates, and replication.
The Leader can revert back to Follower if it has outdated _term_ which is a monotonically increasing value for data consistency used in Raft~@ongaro_2014_raft.
A new Leader is chosen among all nodes at initialization phase and when the existing Leader fails, see @fig:states.

Follower is the default state, all nodes are initially Followers.
A Follower responds to messages from the Leader and does the computation.
When a Follower detects Leader failure, it becomes a Candidate and starts a leader election.

The can be multiple Candidates at the same time.
Each time a node becomes a Candidate, it increases its term and requests votes from all other nodes.
A node receiving vote request will vote for a candidate only if the candidate has up-to-date log, determined by last entry of the candidates log and term @ongaro_2014_raft.
Additionally, a node can vote only once per term.
Candidates are identified by random UUIDs that are attached to vote requests.
There are $2^122$ different random UUIDs~@uuid_rfc9562, hence the possibility of duplicate UUIDs is negligible.


If a Candidate receives vote from the majority of nodes, it becomes a Leader and all other Candidates revert back to Follower.
If none of the Candidates receive majority votes, all Candidates wait until their random timeout is exceeded and start a new election.
This repeats until a Leader is elected.


#figure(
  include "/docs/final_report/images/node_states.typ",
  caption: [Node states, simplified version of~@ongaro_2014_raft[Figure 4]],
)<fig:node_states>
