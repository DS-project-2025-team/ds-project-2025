== Performance

The following tests are done with an 8 core processor Ryzen 7 5700X.
The system is at Git commit `de4cc777227c6a679994158bff57d9fcb40a8b2c` at the time of testing.

=== Startup time

With local Kafka instance already started, starting a node takes about 10-15 seconds.
We counted the time from running the command until the first log line of the form
```log
[INFO] 12:34:56: ...
```
is outputted.
The aiokafka package prints some logs before our logs but it has clearly different format.

We suspect that the slow startup time is caused by creating many connections to Kafka instance.

=== Computation<sect:computation>

The system is already in running in ready state before we sent inputs.

We tested our prototype with the following 3-SAT formula
```json
[
  (1, 2, 3),
  (1, 2, -3),
  (1, -2, 3),
  (1, -2, -3),
  (-1, 2, 3),
  (-1, 2, -3),
  (-1, -2, 3),
  (-1, -2, -3),
  (-5, 6, 10),
  (1, 19, -20),
  (-20, 18, -19),
]
```
Each $3$-tuple corresponds to one clause of the SAT formula.
The variables are represented by their index, negation is represented by minus sign.
For example,
$
   2 & |->x_2 \
  -5 & |->not x_5
$
The formula is not satisfiable.
Additionally, for ease of testing, all assignments $[0,2^20)$ are checked instead of skipping assignments not affecting the used variables.

The results are shown in @table:benchmark.
Each configuration is ran twice and the result is the average.

We note that the system is much slower than running the computation directly.
This is probably caused by too small tasks and long wait time between task assignments.
Currently, the Leader assigns tasks every 2 seconds and splits the full interval into subintervals of size $2^18$ (`SUBINTERVAL_EXPONENT` in `src/config.py`).
In the test case, it is splitted to 4 tasks which leads to 8 second waiting time.
This explains most of the 10 second overhead visible in @table:benchmark.

#figure(
  table(
    columns: (auto, auto),
    align: (left, right),
    inset: 0.5em,
    table.header([*Configuration*], [*Time (s)*]),
    [Directly through function call], [2.3],
    [1 Leader + 2 Follower], [12],
    [1 Leader + 1 Follower], [13],
  ),
  caption: [Performance of the system with different configurations.],
)<table:benchmark>

The script for running tests directly with function calls can be found in `src/benchmark/sat_parallel.py`.
The script be ran in project root directory with
```sh
PYTHONPATH=src uv run src/benchmark/sat_parallel.py
```
