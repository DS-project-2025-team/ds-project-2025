== Reporting individual tasks

The freshness of REPORT messages are identified by the hash of the SAT formula instead of a hash indicating Follower state.

This allows reporting individual tasks instead of all at once and allows utilizing the message broker for at-most-once delivery of tasks.
The Leader also no longer needs to track how the tasks are assigned to Followers.
