from scipy.signal import find_peaks


def detect_peaks(x, y):

    peaks, properties = find_peaks(
        y,
        prominence=30,
        distance=100,
        width=15
    )

    return peaks, properties