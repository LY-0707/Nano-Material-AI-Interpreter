# src/sem_analysis/descriptor.py


# ======================
# SEM Descriptor
# ======================

def extract_sem_descriptor(
    meta,
    features
):
    """
    Generate machine-readable
    SEM descriptor for
    multimodal analysis.
    """

    # No particle case
    if features["count"] == 0:

        return {
            "sample_name":
                f"{meta['material']}_"
                f"{meta['sample_id']}",

            "particle_count": 0,

            "particle_size_nm": 0,

            "variance": 0,

            "size_class":
                "unknown",

            "distribution":
                "unknown",

            "aggregation":
                "unknown",

            "porosity": 0,

            "shape":
                "unknown"
        }

    size = features["avg_size"]
    var = features["variance"]

    # ======================
    # Size Classification
    # ======================

    if size < 50:
        size_class = "small"

    elif size < 200:
        size_class = "medium"

    else:
        size_class = "large"

    # ======================
    # Distribution
    # ======================

    if var < 500:
        distribution = "uniform"

    elif var < 2000:
        distribution = (
            "moderately uniform"
        )

    else:
        distribution = (
            "non-uniform"
        )

    # ======================
    # Aggregation
    # ======================

    if var < 1000:
        aggregation = "low"

    elif var < 3000:
        aggregation = "moderate"

    else:
        aggregation = "high"

    # ======================
    # Descriptor Output
    # ======================

    descriptor = {

        "sample_name":
            f"{meta['material']}_"
            f"{meta['sample_id']}",

        "particle_count":
            features["count"],

        "particle_size_nm":
            round(size, 2),

        "variance":
            round(var, 2),

        "size_class":
            size_class,

        "distribution":
            distribution,

        "aggregation":
            aggregation,

        # 临时占位
        "porosity":
            0,

        # 后续升级
        "shape":
            "unknown"
    }

    return descriptor


# ======================
# Text Description
# ======================

def generate_description(
    meta,
    features
):
    """
    Human-readable
    SEM report.
    """

    descriptor = (
        extract_sem_descriptor(
            meta,
            features
        )
    )

    if (
        descriptor[
            "particle_count"
        ] == 0
    ):
        return (
            "No particles detected."
        )

    return f"""
Sample:
{descriptor['sample_name']}

Morphology Analysis:
- Particle count:
{descriptor['particle_count']}

- Average size:
{descriptor['size_class']}
(area ~
{descriptor['particle_size_nm']:.2f})

- Distribution:
{descriptor['distribution']}

- Aggregation level:
{descriptor['aggregation']}
"""