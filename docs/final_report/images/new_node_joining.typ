#import "@preview/diagraph:0.3.6": raw-render

#raw-render(
  ```dot
  digraph {    
    subgraph {
      cluster=true
      L
      F_1
      F_2
    }
    {
      edge [style=invisible, arrowhead=none]
      L->{F_1,F_2}
    }
    N->L [label="JOIN"]
    L->N [label="ASSIGN tasks"]
  }
  ```
)