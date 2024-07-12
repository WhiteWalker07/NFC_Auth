import numpy as np
import wave
import matplotlib.pyplot as plt
from scipy.fftpack import fft

# Parameters
filename = "last_5_minutes.wav"
N_users = 15
# Open the audio file
wf = wave.open(filename, 'rb')

# Read the audio file properties
n_channels = wf.getnchannels()
sampwidth = wf.getsampwidth()
framerate = wf.getframerate()
n_frames = wf.getnframes()
duration = n_frames / framerate

# Read the audio data
audio_data = wf.readframes(n_frames)
wf.close()

# Convert the audio data to a numpy array
audio_array = np.frombuffer(audio_data, dtype=np.int16)

# Compute the FFT
fft_result = fft(audio_array)

# Calculate frequencies
frequencies = np.fft.fftfreq(len(fft_result), 1/framerate)

# Only take the positive frequencies (since FFT output is symmetric)
positive_freq_indices = np.where(frequencies >= 0)
positive_frequencies = frequencies[positive_freq_indices]
positive_fft_result = np.abs(fft_result[positive_freq_indices])

# Plot the FFT result (optional)
plt.figure(figsize=(10, 6))
plt.plot(positive_frequencies, positive_fft_result)
plt.title('FFT of Audio Signal')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')
plt.show()

# Store the result in an array
fft_array = np.column_stack((positive_frequencies, positive_fft_result))

print("FFT computation complete. Result stored in 'fft_array'.")
print(len(fft_result),fft_result.itemsize)