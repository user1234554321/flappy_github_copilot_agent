import wave
import numpy as np

# Function to create a simple sound

def create_sound(filename, frequency, duration, volume=0.5):
    framerate = 44100
    t = np.linspace(0, duration, int(framerate * duration))
    data = (volume * np.sin(2 * np.pi * frequency * t)).astype(np.float32)

    with wave.open(filename, 'w') as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(framerate)
        f.writeframes((data * 32767).astype(np.int16).tobytes())

# Create flap sound
create_sound('flap.wav', frequency=440, duration=0.1)

# Create score sound
create_sound('score.wav', frequency=880, duration=0.1)

# Create hit sound
create_sound('hit.wav', frequency=220, duration=0.1)