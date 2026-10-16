# Measure-Mate — Setup & Development Guide

This directory contains the core engine, web application, neural network inference scripts, and frontend templates for Measure-Mate.

---

## ⚡ Quick Start

### 1. One-Click Start (Windows)
Double-click `Run Measure Mate.bat`. It will:
1. Locate and activate the `hmr` Conda environment.
2. Launch the Flask server on port `5000`.
3. Automatically open `http://127.0.0.1:5000` in your default web browser.

---

### 2. Manual Start

```bash
# 1. Activate the conda environment
conda activate hmr

# 2. Navigate to this directory
cd Human-Body-Measurements-using-Computer-Vision

# 3. Start the Flask server
python app.py
```

Navigate to: `http://127.0.0.1:5000`

---

## 📦 Requirements & Environment Setup

```bash
# Create Python 3.7 environment
conda create -n hmr python=3.7 -y
conda activate hmr

# Install pinned dependencies
pip install -r requirements.txt
```

---

## 🖥️ Command-Line Interface (CLI)

Run inference on standalone images with:

```bash
python inference.py -i <path_to_image> -ht <height_in_inches>
```

- `-i`: Path to the input image (PNG/JPG).
- `-ht`: Subject height in inches (used as reference scale).

Outputs the reconstructed 3D body mesh to `test.obj` and prints all 11 body measurements to the terminal.

---

## 🌐 Endpoints & Pages

- `GET /` — Studio Lookbook Home Page
- `GET /how-it-works` — 4-Stage Architectural Pipeline
- `GET /measurements` — 3D Measurement Visualizer & Analysis Workspace
- `GET /api` — Developer API Preview & Early Access Form
- `GET /model.obj` — Serves the latest reconstructed 3D mesh (`test.obj`)
- `POST /process` — Image upload & AI measurement inference endpoint