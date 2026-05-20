# src/raman_analysis/loader.py

import numpy as np
import re


def load_raman_txt(file_path):
    """
    Load Raman spectroscopy txt file.

    Supports:
    - EduRaman Pro export
    - tab separated
    - whitespace separated
    - mixed delimiters

    Returns
    -------
    shift : np.ndarray
        Raman shift (cm⁻¹)

    intensity : np.ndarray
        Raman intensity
    """

    rows = []

    with open(
        file_path,
        "r",
        encoding="utf-8",
        errors="ignore"
    ) as f:

        header_found = False

        for line in f:

            line = line.strip()

            # 跳过空行
            if not line:
                continue

            # ===================================
            # 找表头
            # ===================================
            if (
                "ramanshift" in line.lower()
                and
                "intensity" in line.lower()
            ):
                header_found = True
                continue

            # 表头前全部跳过
            if not header_found:
                continue

            # ===================================
            # 自动切分
            # 支持 tab / 空格
            # ===================================
            parts = re.split(
                r"\t+|\s+",
                line
            )

            # EduRaman 至少5列
            if len(parts) < 5:
                continue

            try:
                # 第4列：ramanshift
                shift = float(parts[3])

                # 第5列：intensity
                intensity = float(parts[4])

                rows.append(
                    [shift, intensity]
                )

            except (
                ValueError,
                IndexError
            ):
                continue

    # ===================================
    # Error check
    # ===================================
    if len(rows) == 0:
        raise ValueError(
            "No valid Raman data found."
        )

    data = np.array(
        rows,
        dtype=float
    )

    shift = data[:, 0]
    intensity = data[:, 1]

    # ===================================
    # Debug print
    # ===================================
    print("\nRaman data loaded.")

    print(
        "First 10 Raman shifts:"
    )
    print(
        shift[:10]
    )

    print(
        "\nFirst 10 Intensities:"
    )
    print(
        intensity[:10]
    )

    return (
        shift,
        intensity
    )