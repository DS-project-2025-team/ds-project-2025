= Scalability<sect:scalability>

We have tested our prototype with 3, 4 and 5 nodes.
The Leader election worked fine with all test configurations.
The situation where the Leader fails was tested with different configurations.
That worked well and new Leader was selected in all cases.

Additionally, it is possible to adjust the intervals between APPEND_ENTRIES or ASSIGN messages to reduce the number of messages and support a larger number of nodes.
Adjusting the interval APPEND_ENTRIES also requires adjusting election timeouts which slows down Leader failure detection.

In this section, we measure the performance of our prototype and discuss possible optimizations, for example, strategies to adjust the interval between ASSIGN messages.

#include "performance.typ"
#include "optimizations.typ"
