#import "@preview/diagraph:0.3.6": raw-render

#raw-render(
  ```dot
  digraph {
    rankdir=LR
    L->F [label="1: APPEND_ENTRIES"]
    F->F [label="2: Detects invalid log"]
    F->F [label="3: Reverts to last valid index"]

    F->L [label="4: GET_ENTRIES"]
    L->F [label="5: log entries"]
  }
  ```,
)
