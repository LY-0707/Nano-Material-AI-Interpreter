from .rules import (
    infer_material_state
)

from .templates import (
    HEADER,
    SEM_SECTION,
    RAMAN_SECTION,
    INTERPRETATION_SECTION
)


def generate_material_report(
    sem_result,
    raman_result
):
    """
    Generate multimodal material report.
    """

    report = HEADER

    # ======================
    # SEM Section
    # ======================

    report += SEM_SECTION.format(
        particle_size=sem_result.get(
            "particle_size_nm",
            0
        ),

        porosity=sem_result.get(
            "porosity",
            0
        ),

        shape=sem_result.get(
            "shape",
            "unknown"
        ),

        aggregation=sem_result.get(
            "aggregation",
            "unknown"
        )
    )

    # ======================
    # Raman Section
    # ======================

    ratio = raman_result.get(
        "id_ig_ratio"
    )

    if ratio is None:
        ratio_text = "N/A"
    else:
        ratio_text = (
            f"{ratio:.2f}"
        )

    report += RAMAN_SECTION.format(
        major_peaks=raman_result.get(
            "major_peaks",
            []
        ),

        material_type=raman_result.get(
            "material_type",
            "unknown"
        ),

        crystallinity=raman_result.get(
            "crystallinity",
            "unknown"
        ),

        id_ig_ratio=ratio_text
    )

    # ======================
    # Integrated Interpretation
    # ======================

    interpretation = (
        infer_material_state(
            sem_result,
            raman_result
        )
    )

    report += (
        INTERPRETATION_SECTION
        + interpretation
    )

    return report


def save_report(
    report,
    output_path
):
    """
    Save report to txt file.
    """

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(report)

    print(
        f"\nReport saved:\n"
        f"{output_path}"
    )