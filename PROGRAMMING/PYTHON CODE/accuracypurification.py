# Python code to model purification device accuracy and sensor requirements for claiming 99.9% removal
# This code runs simulations to:
# 1. Model an input contaminant concentration distribution
# 2. Simulate purification stages with given removal efficiencies
# 3. Model sensor measurement error (bias + noise) and compute observed removal %
# 4. Monte Carlo to estimate probability that observed removal >= 99.9%
# 5. Compute required sensor standard deviation (measurement noise) to claim 99.9% with a desired confidence level
#
# The user can change parameters in the "Scenario parameters" section.
#
# This is designed for academic/engineering analysis and to be reproducible.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

np.random.seed(42)

# --------------------------- Scenario parameters ---------------------------
N = 20000  # Monte Carlo trials
input_mean = 100.0         # initial contaminant concentration (units: ppb or mg/L — arbitrary)
input_sd = 5.0             # variability of input concentration (process variability)
stage_efficiencies = [0.90, 0.90, 0.999]  # fractional removal per stage (e.g., 90%, 90%, 99.9%)
# Note: overall removal = 1 - product(1 - efficiency_i) ; for multiplicative removal we model sequential reduction
sensor_bias = 0.0          # systematic measurement bias (same units as concentration)
sensor_sd = 0.05           # relative sensor measurement noise (fraction of true concentration); we'll vary this later
target_removal_pct = 99.9  # target claimed removal percentage
confidence_level = 0.95    # desired probability that observed removal >= target

# --------------------------- Helper functions ---------------------------
def simulate_purification(input_conc, efficiencies):
    """Simulate sequential purification stages returning final concentration."""
    c = input_conc
    for e in efficiencies:
        # each stage removes fraction e of current concentration
        c = c * (1.0 - e)
    return c

def sensor_measure(true_value, rel_sd, bias=0.0):
    """Model sensor measurement with relative Gaussian noise and additive bias."""
    # If true_value == 0, set measurement to bias + small noise proportional to sensor floor
    noise = np.random.normal(loc=0.0, scale=rel_sd * max(true_value, 1e-6))
    return true_value + bias + noise

def compute_removal_pct(in_meas, out_meas):
    """Compute removal percentage from measured input/output concentrations."""
    # Avoid division by zero; if in_meas is 0, treat removal as 100% if out_meas <= tolerance
    if in_meas <= 0:
        return 100.0 if out_meas <= 1e-9 else 0.0
    return max(0.0, min(100.0, (1.0 - out_meas / in_meas) * 100.0))

# --------------------------- Monte Carlo simulation ---------------------------
def run_simulation(N, input_mean, input_sd, efficiencies, sensor_bias, sensor_rel_sd):
    removals = []
    true_in = []
    true_out = []
    meas_in = []
    meas_out = []
    for _ in range(N):
        # sample true input concentration (allow it to be positive)
        t_in = max(0.0, np.random.normal(loc=input_mean, scale=input_sd))
        t_out = simulate_purification(t_in, efficiencies)
        # sensor measurements
        m_in = sensor_measure(t_in, sensor_rel_sd, bias=sensor_bias)
        m_out = sensor_measure(t_out, sensor_rel_sd, bias=sensor_bias)
        rp = compute_removal_pct(m_in, m_out)
        removals.append(rp)
        true_in.append(t_in)
        true_out.append(t_out)
        meas_in.append(m_in)
        meas_out.append(m_out)
    return {
        "removals": np.array(removals),
        "true_in": np.array(true_in),
        "true_out": np.array(true_out),
        "meas_in": np.array(meas_in),
        "meas_out": np.array(meas_out),
    }

# Run baseline simulation
baseline = run_simulation(N, input_mean, input_sd, stage_efficiencies, sensor_bias, sensor_sd)

# Summary statistics for baseline
mean_removal = baseline["removals"].mean()
pct_meeting_target = (baseline["removals"] >= target_removal_pct).mean() * 100.0
median_removal = np.median(baseline["removals"])

summary_df = pd.DataFrame({
    "Metric": ["Mean measured removal (%)", f"Median measured removal (%)", f"% trials with measured removal ≥ {target_removal_pct}%"],
    "Value": [round(mean_removal, 4), round(median_removal, 4), round(pct_meeting_target, 4)]
})

# --------------------------- Find required sensor noise for desired confidence -------------
# We'll sweep sensor relative SD from tiny (0.001) to larger (0.2) and find the minimum sensor_rel_sd
# that yields probability >= confidence_level of observed removal >= target_removal_pct.
rel_sd_values = np.concatenate([np.linspace(0.0005, 0.01, 20), np.linspace(0.01, 0.2, 60)])
probabilities = []
for s in rel_sd_values:
    res = run_simulation(5000, input_mean, input_sd, stage_efficiencies, sensor_bias, s)
    prob = (res["removals"] >= target_removal_pct).mean()
    probabilities.append(prob)

probabilities = np.array(probabilities)
# Find minimum rel_sd such that prob >= confidence_level, if any
if np.any(probabilities >= confidence_level):
    idx = np.where(probabilities >= confidence_level)[0][0]
    required_rel_sd = rel_sd_values[idx]
else:
    required_rel_sd = None

# --------------------------- Present results ---------------------------
print("=== Baseline Simulation Summary ===")
print(summary_df.to_string(index=False))

if required_rel_sd is not None:
    print(f"\nTo achieve at least {int(confidence_level*100)}% confidence that measured removal ≥ {target_removal_pct}%, "
          f"sensor relative SD (1-sigma) must be ≤ {required_rel_sd:.6f} (fraction of measured value).")
else:
    print(f"\nNo sensor relative SD in the tested range (up to {rel_sd_values.max():.3f}) achieved {int(confidence_level*100)}% confidence. "
          "You need more precise sensors or reduce process variability.")

# --------------------------- Plots ---------------------------
# 1) Histogram of measured removal percentages for baseline
plt.figure(figsize=(8,4))
plt.hist(baseline["removals"], bins=120)
plt.title("Histogram of measured removal percentages (baseline sensor noise)")
plt.xlabel("Measured removal (%)")
plt.ylabel("Counts")
plt.tight_layout()
plt.show()

# 2) Probability curve: sensor relative SD vs probability of meeting target
plt.figure(figsize=(8,4))
plt.plot(rel_sd_values, probabilities)
plt.axhline(confidence_level, linestyle='--')
plt.title(f"Probability of measured removal ≥ {target_removal_pct}% vs sensor relative SD")
plt.xlabel("Sensor relative SD (1-sigma, fraction of value)")
plt.ylabel("Probability")
plt.tight_layout()
plt.show()

# 3) Small table of percentiles of measured removal
percentiles = np.percentile(baseline["removals"], [1,5,25,50,75,95,99])
percentile_df = pd.DataFrame({
    "Percentile": ["1%", "5%", "25%", "50%", "75%", "95%", "99%"],
    "Measured removal (%)": np.round(percentiles, 4)
})

import caas_jupyter_tools as cjt
cjt.display_dataframe_to_user("Baseline simulation summary", summary_df)
cjt.display_dataframe_to_user("Measured removal percentiles", percentile_df)

# Also provide a short textual interpretation (printed)
print("\nInterpretation (brief):")
print(f"- With the chosen stage efficiencies {stage_efficiencies} the true overall removal on average is "
      f"{(1 - np.prod([1 - e for e in stage_efficiencies]))*100:.6f}% (theoretical).")
true_overall = (1 - np.prod([1 - e for e in stage_efficiencies]))*100
print(f"- The sensors with relative SD={sensor_sd} produced an average measured removal of {mean_removal:.4f}%, median {median_removal:.4f}%.")
if required_rel_sd is not None:
    print(f"- To claim {target_removal_pct}% removal with {int(confidence_level*100)}% confidence given process variability, sensor 1-sigma must be <= {required_rel_sd:.6f}.")
else:
    print("- Sensor precision in the tested range could not guarantee the target confidence; consider reducing process variability or improving sensors.")
