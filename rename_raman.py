from pathlib import Path
import re

folder = Path("data/raman/raw")

files = list(folder.glob("*.txt"))

for file in files:

    old_name = file.stem

    # ======================
    # 1. 浓度提取 + 统一 ppm
    # ======================
    conc_match = re.search(
        r"(\d+(?:\.\d+)?)\s*(ppb|ppm)",
        old_name,
        re.IGNORECASE
    )

    if conc_match:
        conc_value = float(conc_match.group(1))
        unit = conc_match.group(2).lower()

        # 统一转 ppm
        if unit == "ppb":
            conc = conc_value / 1000
        else:
            conc = conc_value

        conc_str = f"{conc:g}"   # 去掉多余0
        conc_unit = "ppm"

    else:
        conc_str = "unknown"
        conc_unit = ""

    # ======================
    # 2. 银纳米粒子
    # ======================
    if "银" in old_name:

        ag_match = re.search(r"(\d+)\s*银", old_name)

        if ag_match:
            ag = ag_match.group(1)
        else:
            ag = "250"

    else:
        ag = "0"

    # ======================
    # 3. NaI（统一0/1）
    # ======================
    nai = "1" if "NaI" in old_name else "0"

    # ======================
    # 4. 时间统一（ms → s）
    # ======================
    time_match = re.search(
        r"(\d+(?:\.\d+)?)\s*(ms|s)",
        old_name,
        re.IGNORECASE
    )

    if time_match:
        time_value = float(time_match.group(1))
        time_unit = time_match.group(2).lower()

        if time_unit == "ms":
            time_value = time_value / 1000

        time_str = f"{time_value:g}s"

    else:
        time_str = "1s"

    # ======================
    # 5. 构建标准文件名
    # ======================
    base_name = (
        f"MG_{conc_str}ppm_"
        f"Ag{ag}_"
        f"NaI{nai}_"
        f"{time_str}"
    )

    # ======================
    # 6. 避免重复
    # ======================
    rep = 1

    while True:

        new_name = f"{base_name}_rep{rep}.txt"
        new_path = file.parent / new_name

        if not new_path.exists():
            break

        rep += 1

    # ======================
    # 7. 重命名
    # ======================
    file.rename(new_path)

    print(f"{file.name} -> {new_name}")

print("\nNormalization complete.")