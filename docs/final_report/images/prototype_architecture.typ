#import "@preview/diagraph:0.3.6": raw-render

#raw-render(
  ```dot
    digraph {
      node [shape=box]
      edge [arrowhead=vee]

      raft -> network
      raft -> services
      raft -> utils
      raft -> entities

      services -> utils
      services -> entities

      network -> entities
      network -> services
      network -> utils
  }
  ```,
  labels: (
    raft: align(center)[
      raft\
      Raft consensus algorithm
    ],
    network: align(center)[
      network\
      Handles messaging between nodes
    ],
    services: align(center)[
      services\
      Business logic
    ],
    entities: align(center)[
      entities\
      Types and objects, mostly data objects
    ],
    utils: align(center)[
      utils\
      Helper functions
    ],
  ),
),
