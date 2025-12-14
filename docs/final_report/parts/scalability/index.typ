= Scalability

We have tested our prototype with 3, 4 and 5 nodes.
The Leader election worked fine with all test configurations.
The situation where the Leader fails was tested with different configurations.
That worked well and new Leader was selected in all cases.

This section gives performance measurements.
Additionally, we discuss possible optimizations.

#include "performance.typ"
#include "optimizations.typ"
