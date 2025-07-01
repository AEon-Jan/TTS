import os
import time
import redis

redis_host = os.environ.get("REDIS_HOST", "redis")
redis_port = int(os.environ.get("REDIS_PORT", "6379"))
r = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)


def get_api_key():
    return r.get("whisper_api_key") or ""

def main():
    # Placeholder for microphone/WebRTC implementation
    api_key = get_api_key()
    if not api_key:
        print("Whisper API key not configured")
        time.sleep(5)
        return
    print("Sending audio to Whisper API...")
    time.sleep(1)
    print("Received text: hello world")

if __name__ == "__main__":
    main()
