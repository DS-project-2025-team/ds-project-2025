== Workflow

We introduce the workflow from submitting a boolean formula to getting the result, see @fig:workflow.

#figure(
  placement: auto,
  include "/docs/final_report/images/workflow.typ",
  caption: [User initiates a computation.],
)<fig:workflow>

The computation begins when a user submits a boolean formula to the system.
Then the Leader splits the computation into smaller tasks and sending tasks to the message broker, see @work_distribution.

The Followers polls tasks from the message broker and compute them.
When a Follower completes its task it reports the result to the Leader, see @fig:node_work_done.
The Leader keeps sending tasks until a Follower reports satisfiable or all tasks are reported.
When the computation is done, the Leader returns the result to the user.

#figure(
  include "/docs/final_report/images/node_work_done.typ",
  caption: [Follower 1 reports to Leader, message broker omitted.],
)<fig:node_work_done>
