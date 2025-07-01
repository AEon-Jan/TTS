import os
import redis
import time

redis_host = os.environ.get("REDIS_HOST", "redis")
redis_port = int(os.environ.get("REDIS_PORT", "6379"))
r = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)


def get_api_key():
    return r.get("openai_api_key") or ""

IN_QUEUE = "stt_text"
OUT_QUEUE = "tts_queue"


def process(text: str) -> str:
    # Placeholder for OpenAI API call
    return text.upper()


def main():
    while True:
        item = r.lpop(IN_QUEUE)
        if not item:
            time.sleep(1)
            continue
        if not get_api_key():
            print("OpenAI API key not configured")
            time.sleep(5)
            continue
        result = process(item)
        r.rpush(OUT_QUEUE, f"1:{result}")
        print("Processed", item)


if __name__ == "__main__":
    main()
