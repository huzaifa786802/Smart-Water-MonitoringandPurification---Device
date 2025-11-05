import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
# True/reference mercury concentration values in µg/L
true_values = np.array([0.5, 1.0, 2.0, 3.5, 5.0, 7.0, 9.0, 10.0])
# Measured mercury sensor readings in µg/L
measured_values = np.array([0.52, 1.05, 1.95, 3.40, 5.10, 6.80, 8.85, 10.1])
# --- Accuracy Calculation Function ---
def per_sample_accuracy_percent(measured, true):
    measured = np.array(measured)
    true = np.array(true)
    abs_error = np.abs(measured - true)
    accuracy = 100 * (1 - abs_error / true)
    accuracy = np.clip(accuracy, 0, 100)  # prevent negative values
    return accuracy
# --- Compute Metrics ---
accuracy_per_sample = per_sample_accuracy_percent(measured_values, true_values)
mean_accuracy = np.mean(accuracy_per_sample)
mae = mean_absolute_error(true_values, measured_values)
rmse = np.sqrt(mean_squared_error(true_values, measured_values))
r2 = r2_score(true_values, measured_values)
# --- Display Results ---
print("=== Mercury Sensor Accuracy Analysis ===")
print(f"Mean Accuracy: {mean_accuracy:.2f}%")
print(f"Mean Absolute Error (MAE): {mae:.4f} µg/L")
print(f"Root Mean Square Error (RMSE): {rmse:.4f} µg/L")
print(f"R² Score: {r2:.4f}")
# --- Visualization ---
plt.figure(figsize=(10, 5))
plt.plot(true_values, label='True Values', marker='o', color='blue')
plt.plot(measured_values, label='Measured Values', marker='s', color='orange')
plt.title('Mercury Sensor: True vs Measured Values')
plt.xlabel('Sample Number')
plt.ylabel('Mercury Concentration (µg/L)')
plt.legend()
plt.grid(True)
plt.show()
# --- Accuracy Graph ---
plt.figure(figsize=(10, 5))
plt.bar(range(len(accuracy_per_sample)), accuracy_per_sample, color='green', alpha=0.7)
plt.title('Per-Sample Accuracy Percentage (Mercury Sensor)')
plt.xlabel('Sample Number')
plt.ylabel('Accuracy (%)')
plt.ylim(0, 105)
plt.grid(axis='y')
plt.show()