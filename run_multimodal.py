# run_multimodal.py

import os
import sys
import matplotlib.pyplot as plt


# ======================
# Project Path
# ======================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

sys.path.append(BASE_DIR)


# ======================
# Import
# ======================

# Config
from src.utils.config_loader import (
    load_config
)

# SEM
from src.sem_analysis.descriptor import (
    extract_sem_descriptor
)

# Raman
from src.raman_analysis.loader import (
    load_raman_txt
)

from src.raman_analysis.peak_detection import (
    detect_peaks
)

from src.raman_analysis.descriptor import (
    extract_raman_descriptor
)

from src.raman_analysis.material_identifier_v5 import (
    identify_materials_v5,
    summarize_material_results_v5
)

# Multimodal
from src.multimodal.interpreter import (
    generate_material_report
)


# ======================
# Config
# ======================

CONFIG_PATH = os.path.join(
    BASE_DIR,
    "configs",
    "config.yaml"
)

config = load_config(
    CONFIG_PATH
)


# ======================
# Raman Pipeline
# ======================

raman_file = os.path.join(
    BASE_DIR,
    "data",
    "raman",
    "raw",
    "MG_0.1ppm_Ag0_NaI0_1s_rep1.txt"
)

print("\nLoading Raman data...")

shift, intensity = load_raman_txt(
    raman_file
)

print(
    f"Loaded points: {len(shift)}"
)

print(
    f"Intensity max: "
    f"{intensity.max():.2f}"
)


# ----------------------
# Peak Detection
# ----------------------

peak_indices = detect_peaks(
    shift,
    intensity,

    prominence_ratio=config[
        "raman"
    ][
        "peak_detection"
    ][
        "prominence_ratio"
    ],

    min_distance=config[
        "raman"
    ][
        "peak_detection"
    ][
        "min_distance"
    ],

    top_n=config[
        "raman"
    ][
        "peak_detection"
    ][
        "top_n"
    ]
)

print(
    f"Detected peaks: "
    f"{len(peak_indices)}"
)

print("\nPeak positions:")

for p in peak_indices:
    print(
        f"{shift[p]:.1f} cm⁻¹"
    )


# ----------------------
# Material Identification
# ----------------------

detected_peaks = (
    shift[peak_indices]
    .tolist()
)

database_path = os.path.join(
    BASE_DIR,
    "database",
    "material_database.json"
)

material_results = identify_materials_v5(
    detected_peaks=shift[peak_indices].tolist(),
    database_path=os.path.join(
        BASE_DIR,
        "database",
        "material_database.json"
    )
)

material_summary = (
    summarize_material_results_v5(
        material_results
    )
)

print(material_summary)


# ----------------------
# Raman Descriptor
# ----------------------

raman_result = (
    extract_raman_descriptor(
        shift,
        intensity,
        peak_indices
    )
)

# 把材料识别结果并入 Raman descriptor
raman_result[
    "material_candidates"
] = material_results

raman_result[
    "material_summary"
] = material_summary


# ======================
# Raman Visualization
# ======================

plt.figure(
    figsize=(10, 5)
)

plt.plot(
    shift,
    intensity,
    label="Raman Spectrum"
)

plt.scatter(
    shift[peak_indices],
    intensity[peak_indices],
    label="Detected Peaks"
)

plt.xlabel(
    "Raman Shift (cm⁻¹)"
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


# ======================
# SEM Pipeline
# ======================

# mock data
meta = {
    "material":
        "Ag",

    "sample_id":
        "01"
}

features = {
    "count":
        124,

    "avg_size":
        42.6,

    "variance":
        834.2
}

sem_result = (
    extract_sem_descriptor(
        meta,
        features
    )
)


# ======================
# Multimodal Report
# ======================

report = (
    generate_material_report(
        sem_result,
        raman_result
    )
)

# 加入材料识别结果
report += (
    "\n"
    + "=" * 40
    + "\n"
    + material_summary
)

print("\n")
print("=" * 60)
print(report)
print("=" * 60)


# ======================
# Save Report
# ======================

output_dir = os.path.join(
    BASE_DIR,
    "outputs",
    "multimodal"
)

os.makedirs(
    output_dir,
    exist_ok=True
)

report_path = os.path.join(
    output_dir,
    "material_report.txt"
)

with open(
    report_path,
    "w",
    encoding="utf-8"
) as f:

    f.write(report)

print(
    f"\nReport saved:\n"
    f"{report_path}"
)