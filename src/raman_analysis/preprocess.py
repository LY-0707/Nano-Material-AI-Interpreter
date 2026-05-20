import numpy as np
from scipy.signal import savgol_filter


def smooth_signal(x, y):
    """
    Savitzky-Golay smoothing

    Parameters
    ----------
    x : np.ndarray
        Raman shift

    y : np.ndarray
        Raman intensity

    Returns
    -------
    x : np.ndarray
        Raman shift

    y_smooth : np.ndarray
        Smoothed intensity
    """

    x = np.asarray(x)
    y = np.asarray(y)

    x = np.atleast_1d(x).flatten()
    y = np.atleast_1d(y).flatten()

    # 数据太短，不平滑
    if len(y) < 21:
        return x, y

    window_length = min(21, len(y))

    # 必须是奇数
    if window_length % 2 == 0:
        window_length -= 1

    polyorder = min(3, window_length - 1)

    y_smooth = savgol_filter(
        y,
        window_length=window_length,
        polyorder=polyorder
    )

    return x, y_smooth


def baseline_correction(x, y):

    x = np.asarray(
        x,
        dtype=float
    )

    y = np.asarray(
        y,
        dtype=float
    )

    x = np.atleast_1d(x).flatten()
    y = np.atleast_1d(y).flatten()

    if len(y) == 0:
        return x, y

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

    return x, corrected