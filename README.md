# 🛡️ UFSI: User-Friendly Scenario Interface
### Closing the gap between UK road safety rules and real world physics

![Python](https://img.shields.io/badge/python-3.12+-blue.svg)
![CARLA](https://img.shields.io/badge/Simulation-CARLA%200.9.16-green.svg)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-red.svg)

---

## 📖 Overview
The UFSI is a forensic tool built to stress test official UK road safety standards. Many current design manuals, such as the Traffic Signs Manual Chapter 6, still rely on static tables from decades ago. This interface uses the CARLA simulator to account for real world noise like varied human reaction times and high speed vehicle dynamics.

This project specifically targets the "Reality Gap" which is the mismatch between idealised mathematical models and the mechanical or human complexities found on a live roadway.

---

## 🏗️ The Three-Tier Architecture
The system follows a decoupled, three-tier framework. This ensures that road safety inspectors can perform sophisticated audits without needing to write code.

1. **Tier 1: Presentation (Streamlit)**
   This layer features "Forensic Sliders" and Constrained Natural Language (CNL). It maps subjective terms like "Surprise" or "Alert" into quantifiable physics values for the engine.
   
2. **Tier 2: Logic Bridge (Python Subprocess)**
   This part manages the lifecycle of the simulation. It uses a subprocess model to launch worker scripts, which keeps the UI snappy and responsive even when the simulation engine is under heavy load.
   
3. **Tier 3: Physics Engine (CARLA API)**
   This is the heavy lifter that handles high fidelity 3D physics, tire-road friction, and ABS modulation.

---

## ➗ Maths Foundations
To maintain forensic integrity, the system performs three specific transformations to convert a user's intent into simulated reality:

* **Velocity Normalisation:**
  $$v_{ms} = v_{mph} \times 0.44704$$
* **Kinetic Energy Derivation:**
  $$E_k = \frac{1}{2} m v^2$$
* **Potential Energy Inversion (Fall Height):**
  $$h = \frac{E_k}{m \times g}$$
  *(This visualises impact force as a vertical fall from **h** metres.)*

---

## 🚀 Getting Started

### Prerequisites
* **CARLA 0.9.16** (Must be running in server mode)
* **Python 3.12+**
* **High Performance GPU** (Recommended for stable frame rates)

### Installation
1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/your-username/UFSI-Road-Safety.git](https://github.com/your-username/UFSI-Road-Safety.git)
   cd UFSI-Road-Safety
