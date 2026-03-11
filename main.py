# main.py
import numpy as np
from src.molecule import QuantumMolecule
from src.vqe_engine import VQESolver
from src.zne_mitigation import ErrorMitigator
from src.visualization import QuantumDashboard

if __name__ == "__main__":
    print("\n========================================================")
    print(" NISQ-Chem: AI-Orchestrated Quantum Error Mitigation")
    print("========================================================\n")

    # 1. Initialize Hamiltonian
    h2 = QuantumMolecule.hydrogen_model()
    
    # 2. Execute VQE under simulated hardware noise
    solver = VQESolver(molecule=h2, optimizer='COBYLA')
    optimal_params, noisy_energy = solver.run()

    # 3. Apply Zero-Noise Extrapolation
    mitigator = ErrorMitigator(solver=solver, optimal_params=optimal_params)
    zne_energy, improvement = mitigator.extrapolate(method='polynomial', degree=2)

    # 4. Generate the Visual Report
    # We pull the actual energy_history collected inside the solver object
    zne_results = {
        'scales': mitigator.scale_factors,
        'energies': mitigator.measured_energies,
        'exact': h2.exact_energy,
        'zne_val': zne_energy,
        'poly_coeffs': np.polyfit(mitigator.scale_factors, mitigator.measured_energies, 2)
    }
    
    # PASS THE ACTUAL HISTORY HERE:
    QuantumDashboard.generate_report(solver.energy_history, zne_results, molecule_name="H2")

    print("\n--- Final Results ---")
    print(f"Raw Noisy Energy:     {noisy_energy:.5f} Hartree")
    print(f"ZNE Mitigated Energy: {zne_energy:.5f} Hartree")
    print(f"Error Mitigated By:   {improvement:.1f}%")
