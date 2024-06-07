# Messages

All messages are sent in JSON format. The message format is as follows:

```json
{
  "command": "messageType",
  "body": {
    "key1": "value1",
    "key2": "value2"
  }
}
```


List of available messages:
1. [Run Match](messages/run_match.md)
1. [kill Match](messages/stop_match.md)
1. [ping](messages/ping.md)
1. [status](messages/status.md)
1. [score](messages/score.md)