from pathlib import Path
import re
import pandas as pd

# ======================
# 数据目录
# ======================
folder = Path("data/raman/raw")

files = list(folder.glob("*.txt"))

data = []

for file in files:

    name = file.stem

    # ======================
    # 1. 浓度 ppm
    # ======================
    conc_match = re.search(
        r"(\d+(?:\.\d+)?)ppm",
        name,
        re.IGNORECASE
    )

    if conc_match:
        conc = float(conc_match.group(1))
    else:
        conc = None

    # ======================
    # 2. Ag
    # ======================
    ag_match = re.search(r"Ag(\d+)", name)
    ag = int(ag_match.group(1)) if ag_match else 0

    # ======================
    # 3. NaI
    # ======================
    nai_match = re.search(r"NaI(\d+)", name)
    nai = int(nai_match.group(1)) if nai_match else 0

    # ======================
    # 4. 时间
    # ======================
    time_match = re.search(r"(\d+(?:\.\d+)?)s", name)
    time_s = float(time_match.group(1)) if time_match else 1.0

    # ======================
    # 5. 重复编号
    # ======================
    rep_match = re.search(r"rep(\d+)", name)
    rep = int(rep_match.group(1)) if rep_match else 1

    # ======================
    # 6. 数据写入
    # ======================
    data.append({
        "filename": file.name,
        "material": "MG",
        "concentration_ppm": conc,
        "Ag": ag,
        "NaI": nai,
        "time_s": time_s,
        "replicate": rep,
        "path": str(file.resolve())
    })

# ======================
# 保存 metadata
# ======================
df = pd.DataFrame(data)

output_path = Path("data/raman/metadata.csv")
df.to_csv(output_path, index=False, encoding="utf-8-sig")

print(f"metadata saved → {output_path}")
print(df.head())
