from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel
import os
import redis
import uuid
import hashlib

app = FastAPI()

redis_host = os.environ.get("REDIS_HOST", "redis")
redis_port = int(os.environ.get("REDIS_PORT", "6379"))
queue_key = "tts_queue"

CONFIG_KEYS = ["OPENAI_API_KEY", "ELEVENLABS_API_KEY", "WHISPER_API_KEY"]

dr = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)


def verify_token(authorization: str | None = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")
    token = authorization.split()[1]
    if not dr.get(f"session:{token}"):
        raise HTTPException(status_code=401, detail="Unauthorized")
    return token

class QueueItem(BaseModel):
    text: str
    priority: int = 1


class InstallPayload(BaseModel):
    admin_user: str
    admin_pass: str
    OPENAI_API_KEY: str | None = ""
    ELEVENLABS_API_KEY: str | None = ""
    WHISPER_API_KEY: str | None = ""


class LoginPayload(BaseModel):
    username: str
    password: str


class ConfigPayload(BaseModel):
    OPENAI_API_KEY: str | None = ""
    ELEVENLABS_API_KEY: str | None = ""
    WHISPER_API_KEY: str | None = ""


@app.get("/setup/status")
def setup_status():
    return {"installed": dr.exists("installed") == 1}


@app.post("/setup/install")
def setup_install(payload: InstallPayload):
    if dr.exists("installed"):
        raise HTTPException(status_code=400, detail="Already installed")
    dr.set("admin_user", payload.admin_user)
    dr.set("admin_pass", hashlib.sha256(payload.admin_pass.encode()).hexdigest())
    for key in CONFIG_KEYS:
        dr.set(key.lower(), getattr(payload, key))
    dr.set("installed", "1")
    return {"status": "installed"}


@app.post("/auth/login")
def login(data: LoginPayload):
    if not dr.exists("installed"):
        raise HTTPException(status_code=400, detail="Not installed")
    user = dr.get("admin_user")
    pw_hash = dr.get("admin_pass")
    if data.username != user or hashlib.sha256(data.password.encode()).hexdigest() != pw_hash:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = uuid.uuid4().hex
    dr.set(f"session:{token}", "1", ex=86400)
    return {"token": token}


@app.get("/config")
def get_config(token: str = Depends(verify_token)):
    cfg = {k.lower(): dr.get(k.lower()) or "" for k in CONFIG_KEYS}
    return cfg


@app.post("/config")
def update_config(payload: ConfigPayload, token: str = Depends(verify_token)):
    for key in CONFIG_KEYS:
        dr.set(key.lower(), getattr(payload, key))
    return {"status": "updated"}

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
