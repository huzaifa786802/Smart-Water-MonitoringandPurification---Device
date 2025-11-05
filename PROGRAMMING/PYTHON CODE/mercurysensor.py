import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt, medfilt
# 1. Simulate Mercury (Hg²⁺) sensor data (ppb concentration)
np.random.seed(42)
time = np.linspace(0, 60, 300)  # 60 seconds, 300 samples
true_mercury_ppb = 1.0 + 0.5 * np.sin(0.3 * np.pi * time / 10)  # base clean signal
noise = np.random.normal(0, 0.0005, size=time.shape)  # random noise
spikes = np.zeros_like(time)
spikes[np.random.randint(0, len(time), 10)] = np.random.uniform(0.001, 0.002, 10)  # occasional noise spikes
raw_signal = true_mercury_ppb + noise + spikes
# 2. Moving Average Filter
def moving_average(data, window_size=5):
    return np.convolve(data, np.ones(window_size) / window_size, mode='same')
filtered_ma = moving_average(raw_signal, window_size=5)
# 3. Median Filter
filtered_med = medfilt(raw_signal, kernel_size=5)
# 4. Butterworth Low-Pass Filter
def butter_lowpass_filter(data, cutoff, fs, order=5):
    nyq = 0.5 * fs  # Nyquist Frequency
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y = filtfilt(b, a, data)
    return y
fs = 5.0  # Sampling frequency (Hz)
cutoff = 0.5  # Cutoff frequency (Hz)
filtered_butter = butter_lowpass_filter(raw_signal, cutoff, fs, order=4)
# 5. Visualization
plt.figure(figsize=(12, 8))
# Unfiltered Data
plt.subplot(2, 1, 1)
plt.plot(time, raw_signal, color='gray', alpha=0.7, label='Unfiltered (Raw Data)')
plt.plot(time, true_mercury_ppb, color='blue', linewidth=2, label='True Mercury Signal')
plt.title("Mercury (Hg²⁺) Sensor Data - Water Treatment (Unfiltered)")
plt.xlabel("Time (s)")
plt.ylabel("Concentration (ppb)")
plt.legend()
plt.grid(True)
# Filtered Data Comparison
plt.subplot(2, 1, 2)
plt.plot(time, raw_signal, color='gray', alpha=0.3, label='Raw Data')
plt.plot(time, filtered_ma, 'r-', linewidth=1.5, label='Moving Average')
plt.plot(time, filtered_med, 'g-', linewidth=1.5, label='Median Filter')
plt.plot(time, filtered_butter, 'b-', linewidth=2, label='Butterworth (filtfilt)')
plt.title("Filtered Mercury (Hg²⁺) Data - Comparison of Techniques")
plt.xlabel("Time (s)")
plt.ylabel("Concentration (ppb)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()