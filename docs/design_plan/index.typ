#import "template.typ": config

#show: config

= Distributed brute-force 3-SAT solver: Design plan

Names:

The system takes 3-SAT instances like $(x_1 and x_2 not x_3) or (not x_2 and not x_3 and x_4)$ and outputs whether it is satisfiable, that is, can the instance be true with any assignments of boolean values to variables.
The work of checking satisfiability is distributed to multiple nodes.

#include "distributing_work.typ"
