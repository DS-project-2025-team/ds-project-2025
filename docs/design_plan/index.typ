#import "template.typ": config

#show: config

= Distributed brute-force 3-SAT solver: Design plan

#linebreak()

Group number: 8

Names: Asta Björk, Jiahao Li, Petteri Huvio, and Vilho Raatikka.

#linebreak()

- names of team members and one paragraph description of the selected topic and key points related to the required features
- at least one figure explaining the top level (architectural) view of the nodes, their roles and communication between nodes
- more detailed description of the topic and/ or selected solution techniques/methods
- description of different nodes, their roles and functionalities
- description of what messages the nodes need to send and receive to be able to perform their operations.

#pagebreak()

The system takes 3-SAT instances like $(x_1 or x_2 or x_3) and (not x_2 or not x_3 or x_4)$ and outputs whether it is satisfiable, that is, can the instance be true with any assignments of boolean values to variables.
The work of checking satisfiability is distributed to multiple nodes.

#include "distributing_work.typ"

#include "main.typ"
