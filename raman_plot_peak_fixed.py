from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import re


# =========================
# 1. 正确读取 Raman 数据
# =========================
def load_raman(file):

    x = []
    y = []

    with open(file, "r", encoding="utf-8", errors="ignore") as f:

        for line in f:

            line = line.strip()
            if not line:
                continue

            # 用正则按空格/Tab切分
            parts = re.split(r"\s+", line)

            # 必须5列（关键）
            if len(parts) != 5:
                continue

            try:
                # 固定结构解析
                ramanshift = float(parts[3])
                intensity = float(parts[4])

                x.append(ramanshift)
                y.append(intensity)

            except:
                continue

    return np.array(x), np.array(y)


# =========================
# 2. 路径
# =========================
folder = Path(r"C:\Users\LY\Nano-Material-AI-Interpreter\data\raman\raw")

files = list(folder.glob("*.txt"))

plot_dir = folder / "plots"
plot_dir.mkdir(exist_ok=True)

peak_dir = folder / "peak_results"
peak_dir.mkdir(exist_ok=True)


# =========================
# 3. 主循环
# =========================
for file in files:

    try:
        # 读取数据
        x, y = load_raman(file)

        if len(x) == 0:
            print(f"Empty: {file.name}")
            continue

        # baseline correction
        y = y - np.min(y)

        # =========================
        # peak detection
        # =========================
        peaks, _ = find_peaks(
            y,
            height=np.max(y) * 0.1,
            distance=5
        )

        peak_x = x[peaks]
        peak_y = y[peaks]

        # =========================
        # 保存 peak
        # =========================
        np.savetxt(
            peak_dir / f"{file.stem}_peaks.csv",
            np.column_stack([peak_x, peak_y]),
            delimiter=",",
            header="ramanshift,intensity",
            comments=""
        )

        # =========================
        # 绘图
        # =========================
        plt.figure(figsize=(8, 5))

        plt.plot(x, y, linewidth=1)
        plt.scatter(peak_x, peak_y, color="red", s=20)

        plt.xlabel("Raman Shift (cm⁻¹)")
        plt.ylabel("Intensity (a.u.)")
        plt.title(file.stem)

        plt.tight_layout()

        plt.savefig(plot_dir / f"{file.stem}.png", dpi=300)
        plt.close()

        print(f"OK: {file.name}")

    except Exception as e:
        print(f"Failed: {file.name} | {e}")


print("\nAll done.")