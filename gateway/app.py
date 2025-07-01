from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import redis

app = FastAPI()

redis_host = os.environ.get("REDIS_HOST", "redis")
redis_port = int(os.environ.get("REDIS_PORT", "6379"))
queue_key = "tts_queue"

dr = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)

class QueueItem(BaseModel):
    text: str
    priority: int = 1

@app.post("/queue")
def add_queue(item: QueueItem):
    dr.rpush(queue_key, f"{item.priority}:{item.text}")
    return {"status": "queued"}

@app.get("/queue")
def get_queue():
    return {"items": dr.lrange(queue_key, 0, -1)}

@app.post("/toggle")
def toggle_tts(enabled: bool):
    dr.set("tts_enabled", "1" if enabled else "0")
    return {"enabled": enabled}

@app.get("/status")
def status():
    enabled = dr.get("tts_enabled") == "1"
    return {"enabled": enabled, "length": dr.llen(queue_key)}
