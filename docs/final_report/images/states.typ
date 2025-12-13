#import "@preview/diagraph:0.3.6": raw-render

#raw-render(
  ```dot
  digraph {
    LeaderElection [label="Leader election"]
    LeaderFailure [label="Leader failure"]
    FollowerFailure [label="Follower failure"]
    
    Initialization->LeaderElection [label="Decide Leader"]
    LeaderElection->Ready [label="Leader chosen"]
    
    Ready->LeaderFailure [label="Leader failed"]
    LeaderFailure->LeaderElection [label="Decide new leader"]
    
    Ready->FollowerFailure [label="Follower failed"]
    FollowerFailure->Ready [label="Reclaim tasks"]
  }
  ```
)