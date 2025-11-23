# Simple python example using kafka as a message broker
- add voters to kafka configuration : echo "controller.quorum.voters=1@localhost:9093" >> bin/kafka/config/server.properties 
- start kafka by executing : cd <to src> ; bin/kafka/bin/kafka-server-start.sh bin/kafka/config/server.properties
- start nodes :
  - cd <to src/node-messaging> ; (in 3 different terminals)
  - uv run node.py --node-id node-a --peer node-b node-c
  - uv run node.py --node-id node-b --peer node-a node-c
  - uv run node.py --node-id node-c --peer node-a node-b
- stop nodes with ^C
- stop kafka with ^C
