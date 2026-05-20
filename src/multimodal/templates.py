# src/multimodal/templates.py

HEADER = """
Material Analysis Report
========================================
"""

SEM_SECTION = """
SEM Analysis
----------------------------------------
Particle Size: {particle_size:.2f} nm
Porosity: {porosity:.2f}
Morphology: {shape}
Aggregation: {aggregation}

"""

RAMAN_SECTION = """
Raman Analysis
----------------------------------------
Major Peaks: {major_peaks}
Material Type: {material_type}
Crystallinity: {crystallinity}
ID/IG Ratio: {id_ig_ratio}

"""

INTERPRETATION_SECTION = """
========================================
Integrated Interpretation
----------------------------------------
"""