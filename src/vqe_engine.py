# src/vqe_engine.py
import numpy as np
from scipy.optimize import minimize
from qiskit.circuit.library import TwoLocal
from qiskit_aer.primitives import Estimator
from qiskit_aer.noise import NoiseModel, depolarizing_error

class VQESolver:
    """Executes a hybrid Variational Quantum Eigensolver under hardware noise."""
    
    def __init__(self, molecule, optimizer='COBYLA', shots=2048):
        self.molecule = molecule
        self.optimizer = optimizer
        self.shots = shots
        
        # Hardware-efficient ansatz
        self.ansatz = TwoLocal(num_qubits=2, rotation_blocks=['ry', 'rz'], 
                               entanglement_blocks='cz', entanglement='full', reps=1)
        self.num_params = self.ansatz.num_parameters
        
        # Base hardware noise parameters
        self.base_1q_err = 0.01
        self.base_2q_err = 0.05
        self.noise_model = self._build_noise_model(scale=1.0)
        self.energy_history = [] # <--- Add this line

    def _build_noise_model(self, scale):
        """Generates a Qiskit noise model with scaled depolarizing errors."""
        noise_model = NoiseModel()
        err_1q = depolarizing_error(min(self.base_1q_err * scale, 1.0), 1)
        err_2q = depolarizing_error(min(self.base_2q_err * scale, 1.0), 2)
        noise_model.add_all_qubit_quantum_error(err_1q, ['ry', 'rz'])
        noise_model.add_all_qubit_quantum_error(err_2q, ['cz'])
        return noise_model

    def evaluate_energy(self, params, scale=1.0, custom_shots=None):
        """Runs the quantum circuit for a given set of parameters and noise scale."""
        shots = custom_shots if custom_shots else self.shots
        noise_model = self._build_noise_model(scale)
        
        estimator = Estimator(
            backend_options={"noise_model": noise_model},
            run_options={"shots": shots, "seed": 42}
        )
        
        # Using Qiskit Aer V1 API
        job = estimator.run(
            circuits=[self.ansatz], 
            observables=[self.molecule.hamiltonian], 
            parameter_values=[params]
        )
        return job.result().values[0]
    
    def run(self):
        print(f"--- Running Noisy VQE for {self.molecule.name} ---")
        self.energy_history = [] # Reset history
        initial_guess = np.random.default_rng(42).random(self.num_params) * 2 * np.pi
        
        def cost_function(params):
            energy = self.evaluate_energy(params, scale=1.0)
            self.energy_history.append(energy) # <--- Capture the data
            return energy
            
        result = minimize(cost_function, initial_guess, method=self.optimizer, options={'maxiter': 200})
        return result.x, result.fun
