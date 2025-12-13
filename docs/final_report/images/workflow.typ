#import "@preview/diagraph:0.3.6": raw-render

#raw-render(
  ```dot
  digraph {
    MessageBroker [label="Message broker"]

    User->Leader [label="Boolean formula"]
    Leader->MessageBroker [label="Assign tasks"]

    Follower1->MessageBroker [label="poll"]
    MessageBroker->Follower1 [label="task 1"]

    Follower2->MessageBroker [label="poll"]
    MessageBroker->Follower2 [label="task 2"]
  }
  ```,
  labels: (
    Follower1: [Follower $1$],
    Follower2: [Follower $2$],
  ),
)
