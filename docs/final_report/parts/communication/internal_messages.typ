== Internal messages

In _Initialization_ state, all nodes start as Follower and connect to the message broker.
At this point there are no APPEND_ENTRIES messages in the system.
This indicates that there is no Leader in the system.
Because of that the system enters the _Leader election_ state.
The election is done using Raft algorithm with random UUIDs as node IDs.
There are $2^122$ different random UUIDs~@uuid_rfc9562, hence the possibility of duplicate UUIDs is negligible.

After Leader election, the system enters Ready state.
In this state, the Leader takes user inputs and distributes the work to Followers using ASSIGN messages.
The ASSIGN message contains a SAT formula and a subinterval.

When the Follower receives the ASSIGN message it does the computation and sends a REPORT message with the results.
The REPORT includes a formula itself and its hash, subinterval and boolean indicating satisfiability.

When the Leader receives the REPORT message, it compares the hash with the hash of the current formula.
If the hashes match and then compares the formula itself.
If the something does not match, then the message is outdated and the Leader ignores it.

Next, we will discuss the messages related to failures.
Currently, we have identified two error states: _Leader failure_ and _Follower failure_.

The failure handling is based on the principle that recomputing does not change the result, only uncompleted tasks can affect the result.
Particularly, a satisfiable assignment can appear in any subinterval.
Thus, in case of failure, recomputing is always a valid solution.

For detecting both Leader and Follower failures, we use APPEND_ENTRIES messages.
The Leader sends periodically an empty APPEND_ENTRIES to all Followers which must respond with an APPENDENTRY_REPONSE message.
If a Follower does not receive a APPEND_ENTRIES message within a certain time window, it converts it self to CANDIDATE, increases the term, and initiates a Leader election.
If a Follower does not respond within a certain time window, then the Leader appends a "node fail" log entry.

If a Follower receives an APPEND_ENTRIES and detects that it has invalid log compared to the Leader's log, then the system has a Follower failure.
The Follower will try to find the last valid log entry index and revert back to it, see @fig:follower_recovery.

The index can be found by sending index and term of entries to the leader and checking whether the leader has an entry with same index and term.
Raft ensures that if two logs have an entry with same index and term, then all preceding entries are the same~@ongaro_2014_raft.
This property allows using binary search find to find the last valid index.

After reverting, the Follower sends a GET_ENTRIES with the last log index to the Leader which will then send all entries after that index.
Now the Follower is recovered and can continue working.

Lastly, when a new node joins the system, it sets itself to Follower and uses same mechanism to synchonize its state.
The Leader will detect the new node when receiving any message from it.
Then the Leader appends "node join" log entry and (eventually) changes the cluster configuration.

#figure(
  include "/docs/final_report/images/follower_recover.typ",
  caption: [A Follower $F$ recovers from invalid state, reverting process is omitted.],
)<fig:follower_recovery>
