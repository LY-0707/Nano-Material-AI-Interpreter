import os
import sys
import matplotlib.pyplot as plt

sys.path.append(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

from src.raman_analysis.loader import load_raman_txt
from src.raman_analysis.preprocess import (
    smooth_signal,
    baseline_correction
)
from src.raman_analysis.peak_detection import detect_peaks
from src.raman_analysis.descriptor import generate_raman_report


# ======================
# Path
# ======================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

raman_folder = os.path.join(
    BASE_DIR,
    "data",
    "raman",
    "raw"
)

txt_files = [
    f for f in os.listdir(raman_folder)
    if f.endswith(".txt")
]

if not txt_files:
    raise FileNotFoundError(
        "No Raman txt files found."
    )

file_path = os.path.join(
    raman_folder,
    txt_files[0]
)

print("\nUsing Raman file:")
print(file_path)

print("\nExists:")
print(os.path.exists(file_path))


# ======================
# Load Data
# ======================

df = load_raman_txt(file_path)

x = df["shift"].values
y = df["intensity"].values


# ======================
# Preprocessing
# ======================

y_smooth = smooth_signal(y)

y_corrected = baseline_correction(
    y_smooth
)


# ======================
# Peak Detection
# ======================

peaks, _ = detect_peaks(
    x,
    y_corrected
)


# ======================
# Report
# ======================

report = generate_raman_report(
    x,
    peaks
)

print(
    "\n========== RAMAN REPORT ==========\n"
)

print(report)


# ======================
# Plot
# ======================

plt.figure(figsize=(12, 7))

# raw spectrum
plt.plot(
    x,
    y,
    alpha=0.4,
    label="Raw Spectrum"
)

# smoothed spectrum
plt.plot(
    x,
    y_smooth,
    label="Smoothed"
)

# corrected spectrum
plt.plot(
    x,
    y_corrected,
    label="Baseline Corrected"
)

# peaks
plt.scatter(
    x[peaks],
    y_corrected[peaks]
)

# annotate peaks
for p in peaks:

    plt.annotate(
        f"{x[p]:.0f}",
        (
            x[p],
            y_corrected[p]
        ),
        textcoords="offset points",
        xytext=(0, 10),
        ha="center"
    )

plt.xlabel(
    "Raman Shift (cm$^{-1}$)"
)

plt.ylabel(
    "Intensity"
)

plt.title(
    "Raman Peak Detection"
)

plt.legend()

plt.tight_layout()

plt.show()