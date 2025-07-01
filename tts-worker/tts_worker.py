import os
import redis
import time

redis_host = os.environ.get("REDIS_HOST", "redis")
redis_port = int(os.environ.get("REDIS_PORT", "6379"))
r = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)


def get_api_key():
    return r.get("elevenlabs_api_key") or ""

QUEUE = "tts_queue"


def synthesize(text: str) -> str:
    # Placeholder for ElevenLabs API call
    print("Synthesizing", text)
    return f"audio/{text[:10]}.wav"


def main():
    while True:
        item = r.lpop(QUEUE)
        if not item:
            time.sleep(1)
            continue
        if not get_api_key():
            print("ElevenLabs API key not configured")
            time.sleep(5)
            continue
        _, text = item.split(":", 1)
        path = synthesize(text)
        r.rpush("audio_ready", path)
        print("Generated", path)

if __name__ == "__main__":
    main()
