= Communication and system states<sect:communication_and_system_state>

The system has two types of messages: external and internal.
The former is for interactions between users and the system.
The latter is for interactions between nodes within the system.
The available messages depend on the state of the system.

@fig:states shows the states and state transitions of the system.
There should be more states for different failures and transitions depending on how they are handled but they are omitted from the figure for clarity.

#figure(
  include "/docs/final_report/images/states.typ",
  caption: [System states and transitions.],
)<fig:states>

In this section, we will discuss the messages by system state and give a summary of the messaging protocol.

#include "initialization.typ"
#include "ready.typ"
#include "failures.typ"
#include "messaging_protocol.typ"
