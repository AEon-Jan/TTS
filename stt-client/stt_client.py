import os
import time

WHISPER_API_KEY = os.getenv("WHISPER_API_KEY", "")

def main():
    # Placeholder for microphone/WebRTC implementation
    print("Sending audio to Whisper API...")
    time.sleep(1)
    print("Received text: hello world")

if __name__ == "__main__":
    main()
