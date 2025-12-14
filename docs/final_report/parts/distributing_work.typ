= Work distribution algorithm<sect:work_distribution>

In this section, we first describe how our problem can be divided into smaller parts.
Next, we give a simple queue-based algorithm that handles Follower failures automatically.
Lastly, we discuss practical implementation of the algorithm using Kafka message broker.

== Creating search intervals

Let $x_1,...,x_n$ be the boolean variables. Each assignment of boolean values can be represented as a bit sequence $(b_1,...,b_n)$ such that $x_i=b_i$ for all $i in {1,...,n}$.
Each bit sequence is also a binary representation of an integer.
Now, the possible assignments are all $n$-bit integers ${0b 0...0,0b 0...01,...,0b 1...1}$, that is, all the integers in the interval $[0,2^n-1]$.

The Leader splits the interval into contiguous subintervals, each representing one task.
Each of these intervals can be checked individually.
Then we can pass a 3-SAT instance of variables $x_1,...,x_n$ and assign subintervals to the nodes.
Now, satisfiability can be checked in parallel.

== Task queue algorithm

Suppose that we have $n$ tasks and the aim is to assign tasks such every task will be computed eventually.
For simplicity, we identify the tasks with integers $1, ..., n$.

Let $Q$ be a queue of tasks (not the queue of formulas) and $L$ a list of boolean variables such that $L[i]$ indicates whether the task $i$ is completed.

The distributing algorithm works as follows:
+ While $Q$ is not empty:
  + Pop the first task $t$ from $Q$.
  + If $t$ is completed, then repeat the previous step
  + Assign the task $t$ via Kafka multicast
  + Append $t$ to the end of $Q$
  + Whenever a task $t'$ is completed, mark $t'$ as completed.

With this approach, Follower failures do not require explicit handling.
Tasks assigned to a failed node will be reassigned eventually.

Additionally, the Leader does not have to know which tasks are assigned to which Followers and which Followers are alive.
The Leader only need to store the queue of tasks (subintervals), and the list of completed tasks.
This allows assigning tasks using the multicast functionality provided by message brokers i.e. Kafka in our case.

== Multicast assignment via Kafka

The Leader repeatedly sends tasks to all Followers via the message broker and with some fixed time interval $d$, see @sect:task_assignment for other choices of~$d$.
The at-most-once delivery provided by Kafka will ensure that at most one Follower receives the task.
Since Kafka is poll-based, it can guarantee at-most-once delivery by disabling retries.
After a Follower completes its task, it reports to the Leader which marks the task completed.
