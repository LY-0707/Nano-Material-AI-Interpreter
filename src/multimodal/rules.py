def infer_material_state(
    sem,
    raman
):
    """
    Rule-based multimodal interpretation.
    """

    interpretations = []

    # ======================
    # SEM-based rules
    # ======================

    particle_size = sem.get(
        "particle_size_nm",
        0
    )

    aggregation = sem.get(
        "aggregation",
        "unknown"
    )

    if particle_size < 100:
        interpretations.append(
            "Nanostructured morphology detected."
        )

    if aggregation == "high":
        interpretations.append(
            "Strong particle aggregation observed."
        )

    elif aggregation == "moderate":
        interpretations.append(
            "Moderate aggregation detected."
        )

    elif aggregation == "low":
        interpretations.append(
            "Low aggregation observed."
        )

    # ======================
    # Raman-based rules
    # ======================

    material_type = raman.get(
        "material_type",
        "unknown"
    )

    crystallinity = raman.get(
        "crystallinity",
        "unknown"
    )

    id_ig_ratio = raman.get(
        "id_ig_ratio"
    )

    if material_type != "unknown":
        interpretations.append(
            f"Raman suggests "
            f"{material_type}."
        )

    if crystallinity != "unknown":
        interpretations.append(
            f"Crystallinity is "
            f"{crystallinity}."
        )

    # Graphitic carbon logic
    if id_ig_ratio is not None:

        if id_ig_ratio < 1:
            interpretations.append(
                "Relatively ordered graphitic structure."
            )

        else:
            interpretations.append(
                "Higher structural disorder detected."
            )

    # ======================
    # Final output
    # ======================

    if len(
        interpretations
    ) == 0:

        return (
            "No significant "
            "material features detected."
        )

    return "\n- " + "\n- ".join(
        interpretations
    )