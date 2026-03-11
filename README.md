![ZNE Results](vqe_zne_report.png)
# NISQ-Chem: Hardware-Resilient Quantum Molecular Solver

This repository demonstrates a hybrid classical-quantum computational pipeline using a Variational Quantum Eigensolver (VQE) paired with active Zero-Noise Extrapolation (ZNE). It mathematically recovers accurate molecular ground-state energies from highly noisy simulated quantum hardware.

## ⚛️ Motivation & Bioengineering Context

Translating computational biochemistry into real-world solutions requires highly accurate physical models. When designing *de novo* peptide macrocycles or targeting complex catalytic domains, we currently rely on classical force fields (via OpenMM or Rosetta). While powerful for large-scale dynamics, classical approximations fundamentally fail to capture raw, heavily correlated quantum electron dynamics.

Quantum algorithms like VQE offer a pathway to exact energy calculations, but current Noisy Intermediate-Scale Quantum (NISQ) hardware is too unstable for practical bioengineering workflows.

**This project is a foundational proof-of-concept.** It scales down to a 2-qubit hydrogen model to isolate and solve the hardware noise problem. By mathematically reconstructing the zero-noise limit from simulated depolarizing hardware errors, it provides the architectural blueprint for extracting quantum-accurate parameters that could eventually feed into classical molecular dynamics pipelines.

## 🧠 Development Methodology

The physical architecture and mathematical validation of this pipeline were designed by the author, while the syntactical implementation was accelerated using AI-assisted programming. This approach highlights modern rapid prototyping workflows in computational physics.

## 🚀 Pipeline Features

* **Object-Oriented Architecture:** Modular classes separating the Hamiltonian definition, the quantum execution loop, and the classical post-processing.
* **Hardware Noise Simulation:** Utilizes Qiskit Aer to inject realistic depolarizing errors (1% single-qubit, 5% two-qubit) typical of current superconducting processors.
* **Polynomial ZNE:** Actively scales the hardware error matrix and fits a polynomial regression curve to mathematically extrapolate the theoretical noise-free energy intercept.
* **Demonstrated Recovery:** In simulation, the ZNE module successfully mitigated hardware error by **>81%**, dropping the measurement error from roughly 70 mHa down to 13 mHa.

## ⚙️ Installation & Usage

```bash
git clone https://github.com/yourusername/nisq-chem.git
cd nisq-chem
pip install -r requirements.txt

```

```python
from src.molecule import QuantumMolecule
from src.vqe_engine import VQESolver
from src.zne_mitigation import ErrorMitigator

# Initialize Hamiltonian
h2 = QuantumMolecule.hydrogen_model()

# Execute VQE under simulated hardware noise
solver = VQESolver(molecule=h2, optimizer='COBYLA')
optimal_params, noisy_energy = solver.run()

# Apply Zero-Noise Extrapolation
mitigator = ErrorMitigator(solver=solver, optimal_params=optimal_params)
zne_energy, improvement = mitigator.extrapolate(method='polynomial', degree=2)

print(f"Mitigated Energy: {zne_energy} Hartree")

```

## 📝 License

MIT License.

