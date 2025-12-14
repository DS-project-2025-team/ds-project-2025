== Ready

In Ready state, the Leader takes user inputs and distributes the work to Followers using ASSIGN messages.
The ASSIGN message contains a SAT formula and a subinterval.

When the Follower receives the ASSIGN message it does the computation and sends a REPORT message with the results, see @fig:node_work_done
The REPORT includes a formula itself and its hash, subinterval and boolean indicating satisfiability.

When the Leader receives the REPORT message, it compares the hash with the hash of the current formula.
If the hashes match and then compares the formula itself.
If the something does not match, then the message is outdated and the Leader ignores it.
