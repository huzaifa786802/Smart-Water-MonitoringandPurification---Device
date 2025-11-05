import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
# Define functions
def per_sample_accuracy_percent(measured, true, max_error=14.0):
    measured = np.array(measured)
    true = np.array(true)
    abs_err = np.abs(measured - true)
    acc = 100.0 * (1.0 - (abs_err / max_error))
    acc = np.clip(acc, 0.0, 100.0)
    return acc, abs_err
def tolerance_accuracy_percent(measured, true, tol=0.1):
    measured = np.array(measured)
    true = np.array(true)
    abs_err = np.abs(measured - true)
    within = np.sum(abs_err <= tol)
    return 100.0 * within / len(true), within, len(true)
def compute_metrics(measured, true, max_error=14.0, tol_list=(0.1, 0.5)):
    measured = np.array(measured)
    true = np.array(true)
    mae = mean_absolute_error(true, measured)
    mse = mean_squared_error(true, measured)
    rmse = math.sqrt(mse)
    r2 = r2_score(true, measured)
    per_acc, abs_err = per_sample_accuracy_percent(measured, true, max_error=max_error)
    tol_results = {}
    for t in tol_list:
        tol_results[t] = tolerance_accuracy_percent(measured, true, tol=t)
    df = pd.DataFrame({
        "True_pH": true,
        "Measured_pH": measured,
        "Abs_Error": np.round(abs_err, 4),
        f"Accuracy_% (max_error={max_error})": np.round(per_acc, 3)
    })
    summary = {
        "MAE": mae,
        "MSE": mse,
        "RMSE": rmse,
        "R2": r2,
        "Mean_Accuracy_%": np.mean(per_acc),
        "Tolerance_Results": tol_results
    }
    return df, summary
# Example dataset (replace with your real sensor readings)
true_values = [7.00, 6.80, 8.20, 4.50, 9.00, 7.20, 5.50, 3.10, 12.0, 0.5]
measured_values = [7.05, 6.70, 8.50, 4.20, 8.80, 7.00, 5.60, 3.40, 11.6, 0.9]
# Compute metrics
df, summary = compute_metrics(measured_values, true_values, max_error=14.0, tol_list=(0.05, 0.1, 0.5))
# Display textual results
print("=== pH Accuracy Results ===\n")
print(df)
print("\nSummary Metrics:")
for k, v in summary.items():
    if k != "Tolerance_Results":
        print(f"{k}: {v}")
print("\nTolerance-based Accuracy (tol, %, count_within, total):")
for t, res in summary["Tolerance_Results"].items():
    print(f"tol={t}: {res}")
# === Graphs ===
plt.figure(figsize=(15, 10))
# 1️⃣ Accuracy per sample
plt.subplot(3, 1, 1)
plt.plot(df.index + 1, df[f"Accuracy_% (max_error=14.0)"], 'bo-', label='Accuracy % per sample')
plt.title('pH Sensor Accuracy per Sample')
plt.xlabel('Sample Number')
plt.ylabel('Accuracy (%)')
plt.grid(True)
plt.legend()
# 2️⃣ True vs Measured pH (correlation)
plt.subplot(3, 1, 2)
plt.plot(df["True_pH"], df["Measured_pH"], 'go', label='Measured vs True')
plt.plot([0, 14], [0, 14], 'r--', label='Ideal 1:1 Line')
plt.title('True vs Measured pH Comparison')
plt.xlabel('True pH')
plt.ylabel('Measured pH')
plt.legend()
plt.grid(True)

# 3️⃣ Error distribution
plt.subplot(3, 1, 3)
plt.hist(df["Abs_Error"], bins=10, color='orange', edgecolor='black')
plt.title('Absolute Error Distribution')
plt.xlabel('Absolute Error (pH units)')
plt.ylabel('Frequency')
plt.grid(True)
plt.tight_layout()
plt.show()