#import "@preview/diagraph:0.3.6": raw-render

#raw-render(
  ```dot
  digraph {

    Follower->Candidate [label="Start election"]
    Candidate->Follower [label="Leader exists"]
    Candidate->Candidate [label="New election"]
    Candidate->Leader [label="Won election"]
    Leader->Follower [label="Outdated term"]
  }
  ```,
)
