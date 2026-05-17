import numpy as np
from scipy.signal import savgol_filter


def smooth_signal(y):
    """
    Savitzky-Golay smoothing
    """

    if len(y) < 11:
        return y

    return savgol_filter(
        y,
        window_length=21,
        polyorder=3
    )


def baseline_correction(y):
    """
    Simple polynomial baseline correction
    """

    x = np.arange(len(y))

    coeff = np.polyfit(
        x,
        y,
        deg=2
    )

    baseline = np.polyval(
        coeff,
        x
    )

    corrected = y - baseline

    return corrected