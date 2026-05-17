def generate_raman_report(x, peaks):

    report = []

    report.append(
        "Raman Spectrum Analysis"
    )

    report.append(
        "-------------------------"
    )

    for p in peaks:

        peak_pos = x[p]

        interpretation = ""

        # 常见碳材料峰
        if 1300 < peak_pos < 1400:
            interpretation = "D band (defect-related)"

        elif 1550 < peak_pos < 1610:
            interpretation = "G band (graphitic structure)"

        report.append(
            f"Peak at {peak_pos:.1f} cm⁻¹ {interpretation}"
        )

    return "\n".join(report)