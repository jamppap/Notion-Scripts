# Notion-Scripts

Simple Python scripts used in Notion articles. These scripts are educational examples and are not "product ready" programs.

## Purpose

This repository contains simple, illustrative scripts that demonstrate various scientific and engineering calculations. Each script is designed to be straightforward and easy to understand, serving as examples for Notion articles.

## Available Scripts

### 1. Permeability Calculator (`scripts/permeability_calculator.py`)

Calculates complex permeability (μ = μ' - jμ'') from impedance data measured with a Vector Network Analyzer (VNA). This is useful for characterizing magnetic materials like ferrites.

**Features:**
- Calculates complex permeability from impedance measurements
- Supports toroidal core geometry
- Generates frequency response plots
- Includes example usage with simulated data

**Usage:**
```bash
python scripts/permeability_calculator.py
```

## Installation

1. Clone this repository:
```bash
git clone https://github.com/jamppap/Notion-Scripts.git
cd Notion-Scripts
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Requirements

- Python 3.7 or higher
- NumPy
- Matplotlib

## Contributing

These scripts are kept simple intentionally for educational purposes. If you have suggestions for improvements or additional example scripts, feel free to open an issue or submit a pull request.

## License

MIT License - Feel free to use these scripts for educational purposes.
