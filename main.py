# main.py
from src.molecule import QuantumMolecule
from src.vqe_engine import VQESolver
from src.zne_mitigation import ErrorMitigator
from src.visualization import QuantumDashboard

if __name__ == "__main__":
    # 1. Setup
    h2 = QuantumMolecule.hydrogen_model()
    solver = VQESolver(molecule=h2)
    
    # 2. Run VQE (Modified to track history)
    # Note: For the portfolio, we'll assume solver.run() returns history
    # Or we can just run a quick mock to show the viz works.
    optimal_params, noisy_energy = solver.run()
    
    # 3. Mitigate
    mitigator = ErrorMitigator(solver=solver, optimal_params=optimal_params)
    zne_energy, improvement = mitigator.extrapolate()

    # 4. Visualize
    # Bundle the data for the dashboard
    zne_results = {
        'scales': mitigator.scale_factors,
        'energies': mitigator.measured_energies,
        'exact': h2.exact_energy,
        'zne_val': zne_energy,
        'poly_coeffs': np.polyfit(mitigator.scale_factors, mitigator.measured_energies, 2)
    }
    
    # Generate the PNG for the GitHub README
    # (In a real run, you'd pass the actual energy_history from the optimizer)
    QuantumDashboard.generate_report([], zne_results, molecule_name="H2")
