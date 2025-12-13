= Communication

The system has two types of messages: external and internal.
The former is for interactions between users and the system.
The latter is for interactions between nodes within the system.
The available messages depend on the state of the system.

@fig:states shows the states and state transitions of the system.
There might be more states for different failures and transitions depending on how they are handled.
#figure(
  include("/docs/final_report/images/states.typ"),
  caption: [System states and transitions.]
)<fig:states>

#include "external_messages.typ"
#include "internal_messages.typ"
#include "messaging_protocol.typ"