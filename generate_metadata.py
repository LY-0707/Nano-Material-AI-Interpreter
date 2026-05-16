from pathlib import Path
import pandas as pd

# 图像目录
image_dir = Path("data/sem/images")

# 获取所有 tif 文件
files = sorted(image_dir.glob("*.tif"))

data = []

for file in files:

    filename = file.name

    # 判断 raw / annot
    if "raw" in filename.lower():
        image_type = "raw"
    elif "annot" in filename.lower():
        image_type = "annot"
    else:
        image_type = "unknown"

    # 提取 sample_id
    # Ag_NPs_s40_raw.tif → s40
    parts = filename.split("_")

    sample_id = None
    for p in parts:
        if p.lower().startswith("s"):
            sample_id = p.lower()

    data.append({
        "filename": filename,
        "sample_id": sample_id,
        "material": "Ag_NPs",
        "image_type": image_type,
        "condition": "",
        "notes": ""
    })

# 保存 metadata
df = pd.DataFrame(data)

output_path = Path("data/sem/metadata.csv")
df.to_csv(output_path, index=False)

print(f"metadata saved to {output_path}")