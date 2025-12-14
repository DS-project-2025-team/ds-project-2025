== Failures

Next, we will discuss the messages related to failures.
Currently, we have identified two error states: _Leader failure_ and _Follower failure_.

The failure handling is based on the principle that recomputing does not change the result, only uncompleted tasks can affect the result.
Particularly, a satisfiable assignment can appear in any subinterval.
Thus, in case of failure, recomputing is always a valid solution.

=== Leader failure

For detecting both Leader and Follower failures, we use APPEND_ENTRIES messages.
The Leader sends periodically an empty APPEND_ENTRIES to all Followers which must respond with an APPENDENTRY_REPONSE message.

If a Follower does not receive a APPEND_ENTRIES message within a certain time window, it converts it self to CANDIDATE, increases the term, and initiates a Leader election.

=== Follower failure

There are two kind of Follower failures: Follower losing connection to leader and Follower having invalid log.

The Leader detects the first case by APPEND_ENTRIES messages.
If a Follower does not respond to  within a certain time window, then the Leader appends a "node fail" log entry.
We have designed our work distribution algorithm such that the Leader automatically reassigns tasks of a failed Follower, see @sect:work_distribution.
Followers leaving the system are also handled by the same mechanism.

The latter case is detected by the Follower itself when receiving APPEND_ENTRIES messages, see @ongaro_2014_raft.
If a Follower detects that it has invalid log compared to the Leader's log, then it will try to find the last valid log entry index and revert back to that index, see @fig:follower_recovery.

The index can be found by sending index and term of entries to the leader and checking whether the leader has an entry with same index and term.
Raft ensures that if two logs have an entry with same index and term, then all preceding entries are the same~@ongaro_2014_raft.
This property allows using halving the search interval with each check, that is, using binary search to find the last valid index.

After reverting, the Follower sends a GET_ENTRIES with the last log index to the Leader which will respond with all entries after that index.
Now the Follower is recovered and can continue working.

Lastly, when a new node joins the system, it sets itself to Follower and uses same mechanism to synchonize its state.
The Leader will detect the new node when receiving any message from it.
Then the Leader appends "node join" log entry and (eventually) changes the cluster configuration.

#figure(
  include "/docs/final_report/images/follower_recover.typ",
  caption: [A Follower $F$ recovers from invalid state, reverting process is omitted.],
)<fig:follower_recovery>
