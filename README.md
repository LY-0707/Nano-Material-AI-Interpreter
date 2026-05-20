# Nano Material AI Interpreter

An AI-assisted multimodal system for Raman + SEM based material identification and structural interpretation.

## Motivation

Traditional material characterization relies heavily on manual interpretation of Raman spectra and SEM images, which is time-consuming and subjective.

This project explores an AI-assisted pipeline to automatically extract features and infer material properties from multimodal experimental data.

## Features

- **Raman spectrum preprocessing:** Baseline correction (Asymmetric Least Squares) and smoothing (Savitzky-Golay).
- **Peak detection & feature extraction:** High-precision peak finding and Raman shift calculation ($\text{cm}^{-1}$).
- **SEM image-based morphology analysis:** Particle sizing, boundary detection, and shape descriptor extraction.
- **Hybrid Matching Engine:** Combined rule-based expert systems with database matching for material identification.
- **Integrated report generation:** Automated structured markdown export.

## System Architecture

```mermaid
graph TD
    In1[Raw Raman Spectrum] --> B[Raman Preprocessing]
    In2[Raw SEM Image] --> C[SEM Image Processing]

    B --> B1[Baseline Correction]
    B --> B2[Smoothing]
    B --> B3[Peak Detection]

    C --> C1[Noise Reduction]
    C --> C2[Morphology Extraction]

    B3 --> F[Feature Fusion Layer]
    C2 --> F

    F --> G[Material Matching Engine]
    G --> G1[Database Matching]
    G --> G2[Rule-based Inference]

    G --> H[AI Interpretation Module]
    H --> I[Structured Report Generation]


## Pipeline

1. Load Raman / SEM data  
2. Preprocess signals  
3. Extract peaks / morphological features  
4. Material matching (database / model)  
5. Generate structured report

## Example Output

Raman Peaks:
- 519.95 cm^-1
- 959.21 cm^-1

Predicted Material:
- Silicon (Confidence: 100%)

## Installation

git clone https://github.com/LY-0707/Nano-Material-AI-Interpreter.git
cd project
pip install -r requirements.txt

## Usage

python run_multimodal.py

## Tech Stack

- Python
- NumPy / SciPy
- OpenCV
- Matplotlib
- Machine Learning (feature-based classification)

## Future Work

- Improve material classification using deep learning
- Expand database for Raman spectral matching
- Improve SEM morphology quantification
- Build web-based visualization interface