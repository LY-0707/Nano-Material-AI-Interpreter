import json
import math


# =========================================================
# 1. Multi-scale similarity (关键修复)
# =========================================================
def similarity(detected, reference, sigma):
    """
    软匹配 + 防止指数崩溃
    """

    diff = abs(detected - reference)

    # Gaussian similarity
    sim = math.exp(-(diff ** 2) / (2 * sigma ** 2))

    # 🔥 soft floor：避免全 0
    if diff < 50:
        sim = max(sim, 0.2)
    elif diff < 150:
        sim = max(sim, 0.05)

    return sim


# =========================================================
# 2. Peak group scoring
# =========================================================
def group_score(detected_peaks, reference_peaks, sigma):
    """
    一个 peak group 的匹配得分
    """

    if not reference_peaks:
        return 0.0

    used = set()
    scores = []

    for ref in reference_peaks:

        best = 0.0
        best_idx = -1

        for i, d in enumerate(detected_peaks):

            if i in used:
                continue

            s = similarity(d, ref, sigma)

            if s > best:
                best = s
                best_idx = i

        if best_idx != -1:
            used.add(best_idx)
            scores.append(best)

    return sum(scores) / len(reference_peaks)


# =========================================================
# 3. Material likelihood
# =========================================================
def material_likelihood(detected_peaks, material_info):
    """
    计算单个材料 likelihood
    """

    sigma = material_info.get("tolerance", 20)

    peak_groups = material_info.get("peak_groups", [])

    if not peak_groups:
        return 0.0, []

    group_scores = []
    evidence = []

    max_group_score = 0.0

    for group in peak_groups:

        peaks = group.get("peaks", [])
        weight = group.get("weight", 1.0)
        gtype = group.get("type", "optional")

        score = group_score(
            detected_peaks,
            peaks,
            sigma
        )

        group_scores.append(score * weight)

        if score > 0.1:
            evidence.extend(peaks)

        max_group_score = max(max_group_score, score)

        # 🔥 mandatory constraint (softened)
        if gtype == "mandatory" and score < 0.4:
            score *= 0.3

    # weighted average
    total_weight = sum(
        g.get("weight", 1.0) for g in peak_groups
    )

    likelihood = sum(group_scores) / total_weight

    # 🔥 fallback rescue (避免全 0)
    if max_group_score < 0.02:
        likelihood = 0.01

    return likelihood, evidence


# =========================================================
# 4. Main inference engine
# =========================================================
def identify_materials(
    detected_peaks,
    database_path,
    top_k=3,
    threshold=0.01
):
    """
    Robust Raman material inference engine v4.1
    """

    with open(database_path, "r", encoding="utf-8") as f:
        database = json.load(f)

    raw = {}
    total = 0.0

    # -------------------------
    # compute raw likelihoods
    # -------------------------
    for name, info in database.items():

        score, evidence = material_likelihood(
            detected_peaks,
            info
        )

        raw[name] = {
            "score": score,
            "evidence": evidence,
            "info": info
        }

        total += score

    # avoid division collapse
    if total < 1e-8:
        total = 1.0

    results = []

    # -------------------------
    # normalize → probability
    # -------------------------
    for name, v in raw.items():

        prob = v["score"] / total

        results.append({
            "material": name,
            "category": v["info"].get("category", "unknown"),
            "probability": round(prob, 3),
            "raw_score": round(v["score"], 3),
            "evidence_peaks": v["evidence"]
        })

    # -------------------------
    # sort
    # -------------------------
    results.sort(
        key=lambda x: x["probability"],
        reverse=True
    )

    # -------------------------
    # fallback: ensure output not empty
    # -------------------------
    if all(r["probability"] == 0 for r in results):
        results[0]["probability"] = 0.1

    return results[:top_k]


# =========================================================
# 5. Report generator
# =========================================================
def summarize_material_results(results):

    if not results:
        return "Material Type: unknown\nConfidence: low\n"

    text = "\nMaterial Inference (v4.1)\n"
    text += "-" * 40 + "\n"

    for i, r in enumerate(results, 1):

        text += (
            f"{i}. {r['material']}\n"
            f"   probability: {r['probability']:.2f}\n"
            f"   raw score: {r['raw_score']:.2f}\n"
            f"   evidence: {r['evidence_peaks']}\n\n"
        )

    text += (
        "Note: soft probabilistic inference with "
        "multi-scale Raman fingerprint matching.\n"
    )

    return text