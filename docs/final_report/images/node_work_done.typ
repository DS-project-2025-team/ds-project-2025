#import "@preview/diagraph:0.3.6": raw-render

#raw-render(
  ```dot
  digraph {
    node [ordering=out]
    {
      edge [style=invisible, arrowhead=none]
      Leader->{Follower1,Follower2}
      
      Follower1 [label="Follower 1"]
      Follower2 [label="Follower 2"]
    }

    Follower1->Leader [label="REPORT false hash=123"]
  }
  ```
)