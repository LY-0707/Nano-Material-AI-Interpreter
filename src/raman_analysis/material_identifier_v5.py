import json

from .domain_detector import (
    compute_domain_score,
    is_in_domain
)

from .material_identifier_v4 import (
    identify_materials as v4_identify,
    summarize_material_results
)


def identify_materials_v5(
    detected_peaks,
    database_path,
    top_k=3
):
    """
    v5: domain-aware material inference system
    """

    with open(database_path, "r", encoding="utf-8") as f:
        database = json.load(f)

    # =====================================================
    # 1. Domain detection stage (NEW)
    # =====================================================
    domain_score = compute_domain_score(
        detected_peaks,
        database
    )

    in_domain = is_in_domain(domain_score)

    # =====================================================
    # 2. OUT OF DOMAIN CASE
    # =====================================================
    if not in_domain:

        return [{
            "material": "unknown_or_out_of_domain",
            "category": "unknown",
            "probability": 1.0,
            "raw_score": 0.0,
            "evidence_peaks": detected_peaks,
            "domain_score": round(domain_score, 3),
            "note": "Spectrum not covered by current database"
        }]

    # =====================================================
    # 3. IN DOMAIN → use v4 inference
    # =====================================================
    results = v4_identify(
        detected_peaks,
        database_path,
        top_k=top_k
    )

    # attach domain info
    for r in results:
        r["domain_score"] = round(domain_score, 3)
        r["note"] = "in-domain inference"

    return results


def summarize_material_results_v5(results):

    if not results:
        return "No result"

    text = "\nMaterial Inference (v5 - Domain Aware)\n"
    text += "-" * 45 + "\n"

    for i, r in enumerate(results, 1):

        text += (
            f"{i}. {r['material']}\n"
            f"   probability: {r.get('probability', 0):.2f}\n"
            f"   domain_score: {r.get('domain_score', 0):.2f}\n"
            f"   note: {r.get('note','')}\n"
            f"   evidence: {r.get('evidence_peaks', [])}\n\n"
        )

    return text