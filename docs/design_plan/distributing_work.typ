== Distributing work

Let $x_1,...,x_n$ be the boolean variables.

We note that each assignment of boolean values can be represented as a bit sequence $(b_1,...,b_n)$ such that $x_i=b_i$.
Each bit sequence is also a binary representation of an integer.
Now, the possible assignments are all $n$-bit integers ${0b 0...0,0b 0...01,...,0b 1...1}$, that is, all the integers in the interval $[0,2^n-1]$.

Next, we split the interval to equally sized subintervals.
Each of these intervals can be checked individually.
Then we can pass a 3-SAT instance of variables $x_1,...,x_n$ and assign subintervals to nodes.
Now, satisfiability can be checked in parallel.
