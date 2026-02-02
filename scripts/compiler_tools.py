import os
import numpy as np
import sys
from qiskit.quantum_info import Operator
from scipy.linalg import norm
from qiskit import QuantumCircuit
import mpmath

def apply_gridsynth_gates(qc, gate_sequence, qubit):
    total_phase = mpmath.mpf("0.0")
    for g in gate_sequence:
        if g == 'H':
            qc.h(qubit)

        elif g == 'T':
            qc.t(qubit)

        elif g == 'Tdg':
            qc.tdg(qubit)

        elif g == 'S':
            qc.s(qubit)

        elif g == 'Sdg':
            qc.sdg(qubit)

        elif g == 'Z':
            # Z = S^2
            qc.s(qubit)
            qc.s(qubit)

        elif g == 'X':
            # X = H S^2 H
            qc.h(qubit)
            qc.s(qubit)
            qc.s(qubit)
            qc.h(qubit)

        elif g == 'Y':
            # Y = X Z (up to global phase)
            qc.h(qubit)
            qc.s(qubit)
            qc.s(qubit)
            qc.h(qubit)
            qc.s(qubit)
            qc.s(qubit)

        elif g == 'W':
            # W is NOT a gate — only a scalar
            total_phase += mpmath.pi / 4
        else:
            raise ValueError(f"Unknown gridsynth symbol: {g}")
        
def get_metrics(qc, target_unitary):
    """Calculates iQuHACK scoring metrics: T-count and Operator Distance."""
    u_approx = Operator(qc).data
    # d(U, U~) = min_phi || U - e^{i phi} U~ ||_op
    alignment_phase = np.angle(np.trace(target_unitary.conj().T @ u_approx))
    dist = norm(target_unitary - np.exp(1j * alignment_phase) * u_approx, ord=2)
    
    counts = qc.count_ops()
    t_count = counts.get('t', 0) + counts.get('tdg', 0)
    return dist, t_count