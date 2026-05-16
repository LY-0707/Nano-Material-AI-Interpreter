import os

def parse_filename(filename):
    name = os.path.basename(filename).replace(".tif", "").replace(".png", "")
    parts = name.split("_")

    return {
        "material": "_".join(parts[0:2]) if len(parts) > 1 else parts[0],
        "sample_id": parts[2] if len(parts) > 2 else "unknown",
        "type": parts[3] if len(parts) > 3 else "raw"
    }