import cv2

from src.sem_analysis.io import parse_filename
from src.sem_analysis.preprocess import load_image, preprocess
from src.sem_analysis.features import extract_particles, compute_features
from src.sem_analysis.descriptor import generate_description

import os

# ====== 路径 ======
img_path = r"C:\Users\LY\Nano-Material-AI-Interpreter\data\sem\images\Ag_NPs_s10_annot.tif"

# ====== 1. 文件解析 ======
meta = parse_filename(img_path)

# ====== 2. 读图 ======
img = load_image(img_path)

# ====== 3. 预处理 ======
binary = preprocess(img)

# ====== 4. 特征提取 ======
areas = extract_particles(binary)
features = compute_features(areas)

# ====== 5. 生成报告 ======
report = generate_description(meta, features)

print("\n================ SEM ANALYSIS REPORT ================\n")
print(report)