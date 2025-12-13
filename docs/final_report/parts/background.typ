= Background<sect:background>

3‑SAT is a NP‑complete problem where one must determine whether a Boolean formula~$phi$ in conjunctive normal form (CNF) with exactly three literals per clause can be satisfied.
Each literal is either a variable $x_i$ or its negation $not x_i$.

The problem is whether there exists an assignment $(x_1, ..., x_n) in {0, 1}^n$ such that $phi(x_1, ..., x_n)=1$.
That is, given a formula $phi$ with variables $x_1, …, x_n$, a satisfying assignment is an $n$‑bit sequence $(b_1, …, b_n)$ such that substituting $x_i = b_i$ for all $i in {1,...,n}$ makes $phi$ true. 

The brute‑force approach requires checking all $2^n$ assignments. 
For moderately sized $n$ (e.g., $n gt.eq 30$), this becomes infeasible for a single machine.
However, every assignment is independent, making 3‑SAT suitable for parallel computation.

Distributed search mitigates the exponential cost by dividing the assignment interval~$[0, 2^n − 1]$ into subintervals processed in parallel across many _nodes_. 
The independence of tasks simplifies design and enables strong scalability.
