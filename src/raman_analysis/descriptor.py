import numpy as np
from src.raman_analysis.database_match import (
    match_material
)


# ======================
# Peak Assignment
# ======================

RAMAN_REFERENCE = {
    "D band": 1350,
    "G band": 1580,
    "2D band": 2700,
    "Si-O": 465,
    "C-H": 2900
}


def assign_peak_name(
    peak_position,
    tolerance=40
):
    """
    Match Raman peak
    to reference peaks.
    """

    for name, ref_peak in (
        RAMAN_REFERENCE.items()
    ):

        if abs(
            peak_position
            - ref_peak
        ) <= tolerance:

            return name

    return "Unknown"


# ======================
# Descriptor Extraction
# ======================

def extract_raman_descriptor(
    x,
    y_corrected,
    peaks
):
    """
    Generate machine-readable
    Raman descriptor for
    multimodal analysis.
    """

    peak_positions = [
        float(round(x[p], 2))
        for p in peaks
    ]

    peak_intensities = [
        float(y_corrected[p])
        for p in peaks
    ]

    peak_assignments = []

    for pos in peak_positions:

        peak_assignments.append(
            assign_peak_name(pos)
        )

    descriptor = {
        "major_peaks":
            peak_positions,

        "peak_assignments":
            peak_assignments,

        "num_peaks":
            len(peaks),

        "material_type":
            "unknown",

        "peak_ratio_ID_IG":
            None,

        "crystallinity":
            "unknown"
    }

    # ======================
    # Carbon-related logic
    # ======================

    d_index = None
    g_index = None

    for i, peak_name in enumerate(
        peak_assignments
    ):

        if peak_name == "D band":
            d_index = i

        elif peak_name == "G band":
            g_index = i

    # Calculate ID/IG
    if (
        d_index is not None
        and
        g_index is not None
    ):

        I_D = peak_intensities[
            d_index
        ]

        I_G = peak_intensities[
            g_index
        ]

        ratio = round(
            I_D / I_G,
            3
        )

        descriptor[
            "peak_ratio_ID_IG"
        ] = ratio

        descriptor[
            "material_type"
        ] = (
            "graphitic carbon"
        )

        # Simple crystallinity
        if ratio < 0.8:

            descriptor[
                "crystallinity"
            ] = "high"

        elif ratio < 1.2:

            descriptor[
                "crystallinity"
            ] = "moderate"

        else:

            descriptor[
                "crystallinity"
            ] = "low"

    return descriptor


# ======================
# Text Report
# ======================

def generate_raman_report(
    x,
    peaks,
    descriptor=None
):
    """
    Generate human-readable
    Raman report.
    """

    lines = []

    lines.append(
        "Raman Analysis Report"
    )

    lines.append("=" * 40)

    lines.append(
        f"Number of Peaks: "
        f"{len(peaks)}"
    )

    lines.append("")

    lines.append(
        "Detected Peaks:"
    )

    for p in peaks:

        pos = round(
            x[p],
            2
        )

        peak_name = (
            assign_peak_name(pos)
        )

        lines.append(
            f"- {pos} cm^-1 "
            f"({peak_name})"
        )

    # ======================
    # Descriptor Info
    # ======================

    if descriptor is not None:

        lines.append("")
        lines.append("=" * 40)

        lines.append(
            "Material Interpretation"
        )

        lines.append(
            f"Material Type: "
            f"{descriptor['material_type']}"
        )

        ratio = descriptor[
            "peak_ratio_ID_IG"
        ]

        if ratio is not None:

            lines.append(
                f"ID/IG Ratio: "
                f"{ratio}"
            )

        lines.append(
            f"Crystallinity: "
            f"{descriptor['crystallinity']}"
        )

        # ======================
        # Database Matching
        # ======================

        detected_peaks = (
            descriptor[
                "major_peaks"
            ]
        )

        material, confidence = (
            match_material(
                detected_peaks
            )
        )

        lines.append("")
        lines.append("=" * 40)

        lines.append(
            "Database Matching"
        )

        lines.append(
            f"Best Match: "
            f"{material}"
        )

        lines.append(
            f"Confidence: "
            f"{confidence}%"
        )

    return "\n".join(lines)