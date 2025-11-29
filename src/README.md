Running messaging test

- Install uv to svm-11.cs.helsinki.fi, and to, say, svm-11-2.cs.helsinki.fi 
- Install kafka to svm-11.cs.helsinki.fi 
- Clone git repo to both machines as well.


(Instructions can be found from the root level README.md.)

Start producer/consumer messaging test as follows:
- ssh to svm-11.cs.helsinki.fi
- start kafka by executing:

      uv run invoke start-kafka
  
- start consumer:

      cd ds-project-2025/src
  
      uv run python message_consumer_test.py
  
- ssh to, say, svm-11-2.cs.helsinki.fi
- start producer:

      cd ds-project-2025/src

      uv run python message_producer_test.py 
