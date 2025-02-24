import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sounddevice as sd
import scipy.io.wavfile as wavf


# Sampling rate (Hz) - Adjust this according to your audio data if known
sampling_rate = 10000

# Read data from file
with open('received_data_flash.txt', 'r') as file:
    data = file.readlines()
# Extract timestamps and values


timestamps = []
values = []

for line in data:
    parts = line.split(': ')
    timestamps.append(parts[0])
    values.append(int(parts[1]))

# Create a pandas DataFrame
df = pd.DataFrame({'Timestamp': timestamps, 'Value': values})



# Convert the list to a NumPy array
audio_data = np.array(values)

# Plot the audio data
plt.figure(figsize=(14, 5))
plt.plot(audio_data)
plt.title('Audio Waveform')
plt.xlabel('Sample Index')
plt.ylabel('Amplitude')
plt.show()



# Assuming audio_data is your original int64 numpy array
# Convert to float32
audio_data_float32 = audio_data.astype(np.float32)

# Normalize the audio data to the range -1.0 to 1.0
# This assumes the original int64 data is in the full range of int64.
# If it's using a smaller range, adjust the divisor accordingly.
max_int32 = np.iinfo(np.int32).max
aver = np.mean(audio_data_float32)
print (aver)
audio_data_normalized = (audio_data_float32 - aver) / 2000


out_f = 'out_wav.wav'
wavf.write(out_f, sampling_rate, audio_data.astype(np.int16))
#wavf.write(out_f, sampling_rate, audio_data)





# Plot the audio waveform
plt.figure(figsize=(14, 5))
plt.subplot(2, 1, 1)  # 2 rows, 1 column, first plot
plt.plot(audio_data_normalized)
plt.title('Audio Waveform')
plt.xlabel('Sample Index')
plt.ylabel('Amplitude')

# Compute the frequency spectrum using FFT
fft_result = np.fft.rfft(audio_data_normalized)
fft_frequency = np.fft.rfftfreq(len(audio_data_normalized), 1/sampling_rate)

# Plot the frequency spectrum
plt.subplot(2, 1, 2)  # 2 rows, 1 column, second plot
plt.plot(fft_frequency, np.abs(fft_result))
plt.title('Frequency Spectrum')
plt.xlabel('Frequency (Hz)')    
plt.ylabel('Magnitude')

plt.tight_layout()
plt.show()






print('now last plot')
# Perform Fourier transform
n = len(audio_data)
fft_values = np.fft.fft(audio_data_normalized)
frequencies = np.fft.fftfreq(n)
# Plot frequency spectrum
plt.figure(figsize=(10, 6))
plt.plot(np.abs(frequencies[:n//2]), np.abs(fft_values[:n//2])) # Plot only positive frequencies
plt.title('Frequency Spectrum Plot')
plt.xlabel('Frequency (kHz)')
plt.ylabel('Amplitude')
plt.grid(True)
plt.tight_layout()
plt.show()