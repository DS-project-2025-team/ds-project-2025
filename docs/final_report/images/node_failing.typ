#import "@preview/diagraph:0.3.6": raw-render

#raw-render(
  ```dot
  digraph {
    L
    F_1
    F_2
    F_3 [style="dashed"]

    L->F_3 [label="detects failure" arrowhead=none style="dashed"]

    L->{F_1,F_2, L} [label="ASSIGN tasks"]
  }
  ```,
)
