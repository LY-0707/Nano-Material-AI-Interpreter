from scipy.signal import find_peaks
import numpy as np


def detect_peaks(
    x,
    y,
    prominence_ratio=0.05,
    min_distance=10,
    top_n=5
):
    """
    Detect major Raman peaks.

    Parameters
    ----------
    x : np.ndarray
        Raman shift

    y : np.ndarray
        Raman intensity

    prominence_ratio : float
        Relative threshold

    min_distance : int
        Minimum peak distance

    top_n : int
        Keep top N major peaks

    Returns
    -------
    peaks : np.ndarray
        Major peak indices
    """

    prominence_threshold = (
        np.max(y)
        * prominence_ratio
    )

    peaks, properties = find_peaks(
        y,
        prominence=prominence_threshold,
        distance=min_distance
    )

    # 没峰直接返回
    if len(peaks) == 0:
        return peaks

    # 按 prominence 排序
    prominences = properties[
        "prominences"
    ]

    sorted_idx = np.argsort(
        prominences
    )[::-1]

    # 取前 top_n 个
    major_peaks = peaks[
        sorted_idx[:top_n]
    ]

    # 按 Raman shift 排序
    major_peaks = np.sort(
        major_peaks
    )

    return major_peaks