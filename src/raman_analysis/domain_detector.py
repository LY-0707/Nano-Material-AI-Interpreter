import math


def spectral_overlap(detected_peaks, reference_peaks, window=80):
    """
    检查 detected peaks 是否能被 reference 覆盖
    """

    if not detected_peaks or not reference_peaks:
        return 0.0

    matched = 0

    for d in detected_peaks:

        for r in reference_peaks:

            if abs(d - r) <= window:
                matched += 1
                break

    return matched / len(detected_peaks)


def build_global_reference(database):
    """
    把所有材料 peak 汇总成 global space
    """

    all_peaks = []

    for mat in database.values():

        peaks = mat.get("reference_peaks", [])

        all_peaks.extend(peaks)

    return all_peaks


def compute_domain_score(detected_peaks, database):
    """
    判断是否 in-domain
    """

    global_ref = build_global_reference(database)

    return spectral_overlap(
        detected_peaks,
        global_ref,
        window=120  # domain-level宽容窗口
    )


def is_in_domain(domain_score, threshold=0.25):
    """
    是否属于数据库覆盖范围
    """

    return domain_score >= threshold