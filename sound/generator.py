import sounddevice as sd
import numpy as np
from utils import NOTE_MAP


class SoundGenerator:
    def __init__(self):
        self.fs = 44100  # Sampling frequency
        self.frequency = 440  # Default frequency (A4)
        self.phase = 0  # Track the phase between frames
        # Create a sorted list of notes and their frequencies
        self.notes = list(NOTE_MAP.keys())
        self.frequencies = list(NOTE_MAP.values())

    def generate_tone(self, frequency, frames):
        # Generate a tone matching the requested number of frames, using the phase for continuity
        t = np.arange(frames) / self.fs
        tone = 0.5 * np.sin(2 * np.pi * frequency * t + self.phase)
        # Update the phase for the next frame
        self.phase += 2 * np.pi * frequency * frames / self.fs
        self.phase %= 2 * np.pi  # Keep phase within 0 to 2*pi
        return tone

    def start_sound(self, note):
        # Get the frequency for the given note
        frequency = NOTE_MAP[note]
        self.frequency = frequency
        # Start the stream with the callback function
        self.stream = sd.OutputStream(callback=self.callback, samplerate=self.fs, channels=1)
        self.stream.start()

    def stop_sound(self):
        if hasattr(self, "stream") and self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None
        self.phase = 0  # Reset phase when stopping the sound

    def callback(self, outdata, frames, time, status):
        if status:
            print(f"Stream status: {status}")
        # Generate tone data for the number of frames requested
        tone = self.generate_tone(self.frequency, frames)
        outdata[:len(tone)] = tone.reshape(-1, 1)
