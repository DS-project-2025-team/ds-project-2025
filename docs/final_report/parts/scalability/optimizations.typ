== Optimizations

In this section we list optimizations that are done or can be done.

=== Asynchronous messaging and multiprocessing

All messaging in our prototype are asynchronous.
This allows processing messages concurrently, that is, waiting messages in parallel.

Additionally, the computation of different tasks is done in parallel with all processors.
For further optimization, we could run the computation within each task in parallel.
This is not implementend in our prototype.

=== Reindexing sparse variables

By sorting the indexes of variables and relabeling variables like $(x_100,x_6,x_8)|->(x_3,x_1,x_2)$ we can duplicate checks that only differ in variables not in the formula.

This is not implemented in the prototype, since it makes controlling computation time more difficult.
We appended clauses with large variable indexes to non-satisfiable formulas to adjust computation time, which relies on not implementing the optimization.

=== Task assignment

Currently, the Leader node assigns new tasks every $d=2$ seconds and splits the full interval into subintervals of length $2^S$ where $S=18$.
This causes a lot of idling for Followers.

To reduce idling, larger subintervals could be used.
However, if the subintervals are too large, there might not be tasks for all Followers.
In the contrary, if the subintervals are too small, then most of the time is spend on messaging.
Ideally, there should be multiple tasks for each Follower and the computation of each subinterval takes much more time than messaging.

Another optimization would be reducing or updating the delay $d$ between task assignments depending on the performance of Followers.
Like the subinterval size, with too small $d$ the messaging overhead is large and many tasks will be recomputed because reporting tasks takes time.
On the other hand, a large delay $d$ causes a lot of idling.

Next, we assume that parallelization within tasks is implementend and messaging delay is negligible relative to computation time of a task.
Additionally, let $n$ be the number of Followers and $t$ be the average computing time of a task.

Now, in ideal case, each Follower should get a new task immediately after they have completed the previous task.
This could be achieved by sending $n$ tasks with delay $d=t$.
Faster Followers will poll more tasks the message broker.
However, the a whole batch is computed if the a task is computed to be satisfiable but not reported.

Another solutions is sending tasks with delay $d=t\/n$.
In this case the Leader sends less unnecessary tasks while waiting for a satisfiable task.
This can lead to too small delay $d$ and cause previously mentioned issues.

By continuosly measuring the average time $t$, the system can react to node leave and joins.
The Followers can measure their computation time and report them to the Leader.
