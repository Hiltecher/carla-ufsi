# 🛡️ UFSI: User-Friendly Scenario Interface
### *Bridging the Reality Gap in UK Road Safety Validation*

![Python](https://img.shields.io/badge/python-3.12+-blue.svg)
![CARLA](https://img.shields.io/badge/Simulation-CARLA%200.9.16-green.svg)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-red.svg)

---

## 📖 Overview
The **UFSI (User-Friendly Scenario Interface)** is a high-fidelity forensic tool designed to stress-test official UK road safety standards. While current design manuals (like the **Traffic Signs Manual Chapter 6**) rely on static tables, the UFSI utilises the **CARLA Autonomous Vehicle Simulator** to inject real-world noise, such as varying human reaction times and high-speed vehicle dynamics, into safety audits.

This project specifically targets the **Reality Gap**: the discrepancy between idealized mathematical models and the mechanical/human complexities of a live roadway.

---

## 🏗️ The Three-Tier Architecture
The system is built on a decoupled, three-tier framework to ensure that non-technical safety inspectors can perform sophisticated audits without writing a single line of code.

1.  **Tier 1: Presentation (Streamlit)**
    * Features "Forensic Sliders" and **Constrained Natural Language (CNL)**.
    * Translates subjective terms like *"Surprise"* or *"Alert"* into quantifiable physics.
2.  **Tier 2: Logic Bridge (Python Subprocess)**
    * Manages the lifecycle of the simulation.
    * Uses a **Subprocess Model** to launch worker scripts, ensuring the UI remains responsive even if the simulation engine experiences latency.
3.  **Tier 3: Physics Engine (CARLA API)**
    * Handles the high-fidelity 3D physics, tire-road friction, and ABS modulation.

---

## ➗ Mathematical Foundations
To maintain forensic integrity, the system performs three critical transformations to convert user intent into simulated reality:

* **Velocity Normalization:**
  $$v_{ms} = v_{mph} \times 0.44704$$
* **Kinetic Energy Derivation:**
  $$E_k = \frac{1}{2} m v^2$$
* **Potential Energy Inversion (Fall Height):**
  $$h = \frac{E_k}{m \times g}$$
  *(Visualizes impact force as a vertical fall from **h** meters.)*

---

## 🚀 Getting Started

### Prerequisites
* **CARLA 0.9.16** (Must be running in server mode).
* **Python 3.12+**
* **High-Performance GPU** (Recommended for stable frame rates).

### Installation
1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/your-username/UFSI-Road-Safety.git](https://github.com/your-username/UFSI-Road-Safety.git)
    cd UFSI-Road-Safety
    ```
2.  **Install Dependencies:**
    ```bash
    pip install streamlit pandas fpdf carla
    ```

### Launching the System
1.  **Start the CARLA Server:**
    *(Navigate to your CARLA root directory)*
    ```bash
    ./CarlaUE4.sh -quality-level=Low
    ```
2.  **Run the UFSI Dashboard:**
    ```bash
    streamlit run app.py
    ```

---

## 📂 Repository Structure
```text
├── app.py                # Main Tier 1 & 2 Controller (UI + Bridge)
├── test_straight_line.py  # Tier 3 Worker: Stop Test Logic
├── test_hazard.py        # Tier 3 Worker: Following Distance Logic
├── report_stop.py        # Forensic PDF Generation (Braking)
├── report_energy.py      # Forensic PDF Generation (Kinetic)
├── results_data/         # Data Store for PDF & CSV Artifacts
└── assets/               # System architecture & DFD diagrams
