import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt, medfilt
# 1. Simulate Manganese (Mn²⁺) sensor data (mg/L concentration)
np.random.seed(42)
time = np.linspace(0, 60, 300)  # 60 seconds, 300 samples
true_manganese_mgL = 0.1 + 0.05 * np.sin(0.4 * np.pi * time / 10)  # base clean signal
noise = np.random.normal(0, 0.005, size=time.shape)  # random noise
unfiltered_data = true_manganese_mgL + noise  # simulated raw sensor readings   
# 2. Moving Average Filter
def moving_average(data, window_size=5):    
    return np.convolve(data, np.ones(window_size) / window_size, mode='same')
moving_avg_data = moving_average(unfiltered_data, window_size=5)
# 3. Median Filter
median_filtered_data = medfilt(unfiltered_data, kernel_size=5)
# 4. Butterworth Low-Pass Filter
def butter_lowpass_filter(data, cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return filtfilt(b, a, data)
fs = 300 / 60  # sampling frequency = 300 samples / 60 sec = 5 Hz
cutoff = 0.5   # cutoff frequency (Hz)
butter_filtered_data = butter_lowpass_filter(unfiltered_data, cutoff, fs, order=4)
# 5. Visualization
plt.figure(figsize=(12, 8))
plt.plot(time, unfiltered_data, label='Unfiltered (Raw)', color='gray', alpha=0.6)
plt.plot(time, moving_avg_data, label='Moving Average Filtered', linewidth=2)
plt.plot(time, median_filtered_data, label='Median Filtered', linewidth=2)
plt.plot(time, butter_filtered_data, label='Butterworth Filtered', linewidth=2)
plt.title("Manganese (Mn²⁺) Sensor Data — Water Treatment Filtration Comparison", fontsize=14)
plt.xlabel("Time (seconds)", fontsize=12)
plt.ylabel("Manganese Concentration (mg/L)", fontsize=12)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
# 6. Comparison Summary
print("=== Manganese Sensor Data Filtration Comparison Summary ===")
print(f"Unfiltered Mean Mn²⁺: {np.mean(unfiltered_data):.4f} mg/L")
print(f"Moving Average Filtered Mean Mn²⁺: {np.mean(moving_avg_data):.4f} mg/L")
print(f"Median Filtered Mean Mn²⁺: {np.mean(median_filtered_data):.4f} mg/L") 
print(f"Butterworth Filtered Mean Mn²⁺: {np.mean(butter_filtered_data):.4f} mg/L") 
                                          