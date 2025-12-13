== Node join and node failure handling

When a new node or a failed node joins, it becomes a Follower and connects to the message broker.
Additionally, it requests missing entries from Leader.
the Leader assign tasks to it and it becomes a Follower, see @fig:new_node_joining.
Additionally, if a node fails, the Leader reclaims its tasks and reassigns them later, see @fig:node_failing.
#figure(
  include "/docs/final_report/images/new_node_joining.typ",
  caption: [A new node $N$ joins],
)<fig:new_node_joining>

#figure(
  include "/docs/final_report/images/node_failing.typ",
  caption: [An existing node $F_3$ fails],
)<fig:node_failing>

The Followers report the results to the Leader when they complete their computation.
The message contains a boolean value indicating whether the satisfiable assignment in within any of the assigned intervals, see @fig:node_work_done.

