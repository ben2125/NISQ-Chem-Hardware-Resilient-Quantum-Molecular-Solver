![ZNE Results](vqe_zne_report.png)

# NISQ-Chem: Hardware-Resilient Molecular Simulation

This project provides a software pipeline designed to get high-accuracy results from "noisy" quantum computers. It simulates a chemical system (Hydrogen) and uses mathematical error correction to filter out hardware interference.

## 💡 The Problem: "Noisy" Hardware

Quantum computers are currently prone to errors caused by heat and electromagnetic interference—commonly called **noise**. This noise distorts calculations, making it difficult to use quantum computers for precise work like drug discovery or molecular modeling.

## 🛠️ The Solution: Mathematical Error Correction

This pipeline uses a two-step approach to solve the noise problem:

1. **VQE (The Solver):** An algorithm that finds the most stable state of a molecule.
2. **ZNE (The Filter):** A mathematical technique that measures how noise affects the data, then "calculates backward" to predict what the result would look like if the hardware were perfect.

## 🧠 Development Methodology

The physical architecture and mathematical validation of this pipeline were designed by the author, while the syntactical implementation was accelerated using AI-assisted programming. This approach highlights modern rapid prototyping workflows in computational physics—leveraging domain expertise to steer and validate complex models while using AI to handle the heavy lifting of coding.

## 🚀 Key Results

In our tests, the mathematical filter was able to **reduce hardware-induced error by over 81%**. This transformed a distorted, unusable measurement into a result accurate enough for scientific research.

## ⚙️ How to Run Locally

```bash
git clone https://github.com/ben2125/NISQ-Chem.git
cd NISQ-Chem
pip install -r requirements.txt
python main.py

```

## 📝 Future Goals

* Expand the tool to simulate larger, more complex molecules.
* Integrate with standard biology simulation tools (like OpenMM) to use quantum-accurate data in protein design.


## 📝 License

MIT License.

