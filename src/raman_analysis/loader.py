import pandas as pd
import numpy as np


def load_raman_txt(path):
    """
    自动读取拉曼 txt 文件
    取最后两列作为：
    Raman shift & intensity
    """

    data = []

    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:

            line = line.strip()

            if not line:
                continue

            # 用空格/tab拆分
            parts = line.split()

            # 至少两列
            if len(parts) < 2:
                continue

            try:
                # 取最后两列
                shift = float(parts[-2])
                intensity = float(parts[-1])

                data.append([shift, intensity])

            except ValueError:
                # 自动跳过表头
                continue

    df = pd.DataFrame(
        data,
        columns=["shift", "intensity"]
    )

    return df