import os
import cv2
import numpy as np


def load_sem_image(image_path):
    """
    Load SEM image in grayscale.

    Parameters
    ----------
    image_path : str
        Path to SEM image.

    Returns
    -------
    np.ndarray
        Grayscale image.
    """

    image = cv2.imread(
        image_path,
        cv2.IMREAD_GRAYSCALE
    )

    if image is None:
        raise ValueError(
            f"Cannot load image: {image_path}"
        )

    return image


def parse_filename(filename):
    name = (
        os.path.basename(filename)
        .replace(".tif", "")
        .replace(".png", "")
    )

    parts = name.split("_")

    return {
        "material": (
            "_".join(parts[0:2])
            if len(parts) > 1
            else parts[0]
        ),
        "sample_id": (
            parts[2]
            if len(parts) > 2
            else "unknown"
        ),
        "type": (
            parts[3]
            if len(parts) > 3
            else "raw"
        )
    }