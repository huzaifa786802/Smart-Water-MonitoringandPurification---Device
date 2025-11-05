import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt, medfilt
# -------------------------------
# SIMULATION PARAMETERS
# -------------------------------
np.random.seed(42)
t = np.linspace(0, 10, 500)  # Time (10 seconds, 500 samples)
# -------------------------------
# SIMULATED SENSOR DATA
# -------------------------------
# Gold Sensor (e.g., detects conductivity changes due to impurities)
gold_raw = 0.8 + 0.2 * np.sin(2 * np.pi * 0.3 * t) + 0.1 * np.random.randn(len(t))
# Platinum Sensor (e.g., measures oxidation-reduction potential)
platinum_raw = 0.6 + 0.3 * np.sin(2 * np.pi * 0.5 * t) + 0.12 * np.random.randn(len(t))
# -------------------------------
# UNFILTERED DATA (BEFORE FILTRATION)
# -------------------------------
# Representing untreated water (raw signal)
untreated_gold = gold_raw
untreated_platinum = platinum_raw
# -------------------------------
# FILTER FUNCTIONS
# -------------------------------
# 1. Moving Average Filter
def moving_average(signal, window_size=5):
    return np.convolve(signal, np.ones(window_size)/window_size, mode='same')
# 2. Median Filter
def median_filter(signal, kernel_size=5):
    return medfilt(signal, kernel_size=kernel_size)
# 3. Butterworth Low-pass Filter using filtfilt
def butter_lowpass_filter(signal, cutoff=1.0, fs=50.0, order=4):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    filtered_signal = filtfilt(b, a, signal)
    return filtered_signal
# -------------------------------
# APPLY FILTERS (AFTER FILTRATION)
# -------------------------------
# Filtered Gold Sensor (after treatment)
gold_ma = moving_average(gold_raw)
gold_med = median_filter(gold_raw)
gold_butter = butter_lowpass_filter(gold_raw)
# Filtered Platinum Sensor (after treatment)
platinum_ma = moving_average(platinum_raw)
platinum_med = median_filter(platinum_raw)
platinum_butter = butter_lowpass_filter(platinum_raw)
# -------------------------------
# VISUALIZATION
# -------------------------------
plt.figure(figsize=(12, 8))
# --- GOLD SENSOR ---
plt.subplot(2, 1, 1)
plt.plot(t, untreated_gold, 'r--', alpha=0.5, label='Gold Sensor (Unfiltered)')
plt.plot(t, gold_ma, 'b', label='Moving Average')
plt.plot(t, gold_med, 'g', label='Median Filter')
plt.plot(t, gold_butter, 'k', label='Butterworth LPF')
plt.title('Gold Sensor Data - Water Treatment Filtration')
plt.xlabel('Time (s)')
plt.ylabel('Sensor Output (V)')
plt.legend()
plt.grid(True)
# --- PLATINUM SENSOR ---
plt.subplot(2, 1, 2)
plt.plot(t, untreated_platinum, 'r--', alpha=0.5, label='Platinum Sensor (Unfiltered)')
plt.plot(t, platinum_ma, 'b', label='Moving Average')
plt.plot(t, platinum_med, 'g', label='Median Filter')
plt.plot(t, platinum_butter, 'k', label='Butterworth LPF')
plt.title('Platinum Sensor Data - Water Treatment Filtration')
plt.xlabel('Time (s)')
plt.ylabel('Sensor Output (V)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
# -------------------------------
# PRINT SUMMARY
# -------------------------------
print("✅ Simulation Complete")
print("Gold Sensor -> Filtered Mean Values:")
print(f"  Moving Average: {np.mean(gold_ma):.3f}, Median: {np.mean(gold_med):.3f}, Butterworth: {np.mean(gold_butter):.3f}")
print("Platinum Sensor -> Filtered Mean Values:")
print(f"  Moving Average: {np.mean(platinum_ma):.3f}, Median: {np.mean(platinum_med):.3f}, Butterworth: {np.mean(platinum_butter):.3f}")