# Architecture

```mermaid
---
title: Components
---
graph

raft[
    raft
    Raft consensus algorithm
]
network[
    network
    Handles messaging between nodes
]
services[
    services
    Business logic
]
entities[
    entities
    Types and objects, mostly data objects
]
utils[
    utils
    Helper functions
]


raft --> network
raft --> services
raft --> utils
raft --> entities

services --> utils
services --> entities

network --> entities
network --> services
network --> utils
```

The usage of other directories:

- `benchmark`: Performance testing
- `examples`: Prototyping

## Initialization

```mermaid
sequenceDiagram
    participant Node1 as Node 1
    participant MessageBroker
    participant Node2 as Node 2

    Node1 ->> Node1: Follower.run()
    Node2 ->> Node2: Follower.run()

    Node1 ->> Node1: election timeout
    Node1 ->> Node1: Candidate.run()

    Node1 ->> MessageBroker: PING (multicast)
    MessageBroker ->> Node2: PING
    Node2 -->> MessageBroker: PING_RESPONSE
    MessageBroker -->> Node1: PING_RESPONSE

    Node1 ->> Node1: Count nodes

    Node1 ->> MessageBroker: VOTE_REQUEST (multicast)
    MessageBroker ->> Node2:

    Node2 -->> MessageBroker: VOTE
    MessageBroker -->> Node1: VOTE

    Note over Node1: "Majority of votes"
    Node1 ->> Node1: Leader.run()
```
