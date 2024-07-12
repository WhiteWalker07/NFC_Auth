import pyaudio
import numpy as np
import wave
import time
from collections import deque

# Parameters
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 300  # 5 minutes
SAVE_INTERVAL = 5  # Save every 60 seconds

# Initialize PyAudio
p = pyaudio.PyAudio()

# Open stream
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("* Recording audio...")

# Deque to store audio data
buffer = deque(maxlen=int(RATE / CHUNK * RECORD_SECONDS))
last_save_time = time.time()

try:
    while True:
        data = stream.read(CHUNK)
        buffer.append(data)

        current_time = time.time()
        if current_time - last_save_time >= SAVE_INTERVAL:
            filename = "last_5_minutes.wav"
            wf = wave.open(filename, 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(buffer))
            wf.close()
            last_save_time = current_time
except KeyboardInterrupt:
    print("* Stopped recording")

# Close stream
stream.stop_stream()
stream.close()
p.terminate()

print(f"Saved last 5 minutes of audio to {filename}")
