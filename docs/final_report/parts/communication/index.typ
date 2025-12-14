= Communication and system states

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

In this section, we will introduce the external messages and discuss the internal messages by system state.

#include "external_messages.typ"
#include "initialization.typ"
#include "internal_messages.typ"
#include "messaging_protocol.typ"
