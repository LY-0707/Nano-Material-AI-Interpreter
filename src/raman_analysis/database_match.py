import json
import numpy as np


def peak_similarity(
    detected,
    reference,
    tolerance=40
):

    matched = 0

    for p in detected:

        for r in reference:

            if abs(p - r) <= tolerance:
                matched += 1
                break

    return matched / len(reference)


def match_material(
    detected_peaks,
    db_path="database/material_database.json"
):

    with open(
        db_path,
        "r",
        encoding="utf-8"
    ) as f:

        database = json.load(f)

    scores = {}

    for material, info in (
        database.items()
    ):

        similarity = peak_similarity(
            detected_peaks,
            info["reference_peaks"]
        )

        scores[material] = similarity

    best_match = max(
        scores,
        key=scores.get
    )

    confidence = round(
        scores[best_match] * 100,
        1
    )

    return (
        best_match,
        confidence
    )