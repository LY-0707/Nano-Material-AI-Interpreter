def generate_description(meta, features):

    if features["count"] == 0:
        return "No particles detected."

    size = features["avg_size"]
    var = features["variance"]

    if size < 50:
        size_desc = "small"
    elif size < 200:
        size_desc = "medium"
    else:
        size_desc = "large"

    if var < 500:
        dist_desc = "uniform"
    elif var < 2000:
        dist_desc = "moderately uniform"
    else:
        dist_desc = "non-uniform"

    return f"""
Sample: {meta['material']}_{meta['sample_id']}

Morphology Analysis:
- Particle count: {features['count']}
- Average size: {size_desc} (area ~ {features['avg_size']:.2f})
- Distribution: {dist_desc}
- Aggregation level: {'low' if var < 1000 else 'moderate' if var < 3000 else 'high'}
"""