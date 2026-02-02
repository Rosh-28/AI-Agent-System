import redis
import json

r = redis.Redis(host="localhost", port=6379, decode_responses=True)
QUEUE = "agent_queue"

def push_task(task: dict):
    r.rpush(QUEUE, json.dumps(task))

def pop_task(block=True, timeout=5):
    if block:
        item = r.blpop(QUEUE, timeout=timeout)
        return json.loads(item[1]) if item else None
    else:
        item = r.lpop(QUEUE)
        return json.loads(item) if item else None
