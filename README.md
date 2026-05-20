# Nano Material AI Interpreter

An AI-assisted multimodal system for Raman + SEM based material identification and structural interpretation.

---

## Motivation

Traditional material characterization relies heavily on manual interpretation of Raman spectra and SEM images, which is time-consuming and subjective.

This project explores an AI-assisted pipeline to automatically extract features and infer material properties from multimodal experimental data.

---

## Features

- **Raman spectrum preprocessing:** Baseline correction (Asymmetric Least Squares) and smoothing (Savitzky-Golay).
- **Peak detection & feature extraction:** High-precision peak finding and Raman shift calculation (cm⁻¹).
- **SEM image-based morphology analysis:** Particle sizing, boundary detection, and shape descriptor extraction.
- **Hybrid Matching Engine:** Combined rule-based system with database matching for material identification.
- **Integrated report generation:** Automated structured Markdown export.

---

## System Architecture

![alt text](mermaid-diagram.png)

---

## Pipeline

1. Load Raman / SEM data
2. Preprocess signals
3. Extract peaks and morphological features
4. Feature fusion
5. Material identification
6. Generate structured report

---

## Example Output

Raman Peaks:

* 519.95 cm⁻¹
* 959.21 cm⁻¹

Predicted Material:

* Silicon (Confidence: 100%)

---

## Installation

```bash
git clone https://github.com/LY-0707/Nano-Material-AI-Interpreter.git
cd Nano-Material-AI-Interpreter
pip install -r requirements.txt
```

---

## Usage

```bash
python run_multimodal.py
```

---

## Tech Stack

* Python
* NumPy / SciPy
* OpenCV
* Matplotlib
* Feature-based classification

---

## Future Work

* Improve material classification using deep learning
* Expand Raman spectral database
* Improve SEM morphology quantification
* Build web-based visualization interface
