import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
# 1. Calibration and voltage → pH model
S_V_Per_pH = 0.05916  # 59.16 mV/pH at 25°C (Nernst slope)
E0_V = 0.0  # Electrode potential at pH = 7
def voltage_to_pH(voltage_V):
    """Convert electrode voltage (V) to pH."""
    return (E0_V - voltage_V) / S_V_Per_pH
# 2. Filtering functions
def moving_average(data, window_size=5):
    return np.convolve(data, np.ones(window_size)/window_size, mode='valid')
def median_filter(data, kernel_size=5):
    return signal.medfilt(data, kernel_size=kernel_size)
def butterworth_filter(data, cutoff=0.1, fs=1.0, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = signal.butter(order, normal_cutoff, btype='low', analog=False)
    return signal.filtfilt(b, a, data)
# 3. Simulate noisy pH sensor data
def simulate_noisy_pH_data(num_samples=1000, fs=1.0):
    """Simulates pH sensor voltage readings for filtered and unfiltered water."""
    np.random.seed(42)
    t = np.arange(num_samples) / fs
    # Simulate unfiltered (raw) and filtered (treated) water pH signals
    pH_unfiltered = 6.8 + 0.5 * np.sin(2 * np.pi * 0.005 * t) + np.random.normal(0, 0.3, num_samples)
    pH_filtered = 7.0 + 0.1 * np.sin(2 * np.pi * 0.05 * t) + np.random.normal(0, 0.05, num_samples)
    # Convert to electrode voltages (inverse of Nernst equation)
    voltage_unfiltered = E0_V - S_V_Per_pH * pH_unfiltered
    voltage_filtered = E0_V - S_V_Per_pH * pH_filtered
    return t, voltage_unfiltered, voltage_filtered
# 4. Main demonstration
def main():
    fs = 1.0  # Sampling frequency (1 sample/sec)
    num_samples = 1000
    # Simulate voltage data
    t, volt_unfiltered, volt_filtered = simulate_noisy_pH_data(num_samples, fs)
    # Convert back to pH
    pH_unfiltered = voltage_to_pH(volt_unfiltered)
    pH_filtered = voltage_to_pH(volt_filtered)
    # Apply filters to unfiltered data
    pH_un_ma = moving_average(pH_unfiltered, window_size=9)
    pH_un_med = median_filter(pH_unfiltered, kernel_size=7)
    pH_un_but = butterworth_filter(pH_unfiltered, cutoff=0.08, fs=fs, order=5)
    # Adjust time axis for moving average
    t_ma = t[len(t) - len(pH_un_ma):]
    # 5. Visualization
    plt.figure(figsize=(12, 8))
    # --- Unfiltered water (Raw) ---
    plt.subplot(2, 1, 1)
    plt.plot(t, pH_unfiltered, label='Noisy pH Data', alpha=0.4)
    plt.plot(t_ma, pH_un_ma, '--', label='Moving Average', linewidth=2)
    plt.plot(t, pH_un_med, '-.', label='Median Filter', linewidth=2)
    plt.plot(t, pH_un_but, ':', label='Butterworth Filter', linewidth=2)
    plt.title('Unfiltered Water – Raw vs Filtered pH Readings')
    plt.ylabel('pH Level')
    plt.grid(True)
    plt.legend()
    # --- Filtered (treated) water ---
    plt.subplot(2, 1, 2)
    plt.plot(t, pH_filtered, label='Treated Water (Stable)', color='green', alpha=0.8)
    plt.plot(t, pH_filtered, '--', label='Filtered Signal Reference', linewidth=2)
    plt.title('Filtered (Treated) Water – Stable pH Readings')
    plt.xlabel('Time (s)')
    plt.ylabel('pH Level')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()
# Entry point
if __name__ == "__main__":
    main()