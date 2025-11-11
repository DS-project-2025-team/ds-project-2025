# Simple python example using kafka as a message broker
- start kafka by executing : cd <to-dir including docker-compose.yml> ; docker compose up -d
- start nodes :
  - cd <to-dir including node.py> ; (in 3 different terminals)
  - uv run node.py --node-id node-a --peer node-b node-c
  - uv run node.py --node-id node-b --peer node-a node-c
  - uv run node.py --node-id node-c --peer node-a node-b
- stop nodes with ^C
- stop kafka with : docker compose stop
