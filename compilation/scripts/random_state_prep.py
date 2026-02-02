import os
import sys
import numpy as np
import mpmath
from qiskit import QuantumCircuit
from qiskit import qasm3
from qiskit.quantum_info import Operator
from pygridsynth.gridsynth import gridsynth_gates
from qiskit import qasm3
from qiskit.quantum_info import random_statevector

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)
from compiler_tools import apply_gridsynth_gates, get_metrics
from scipy.linalg import expm

# Target Unitary for random (given) state preparation 
target_state = random_statevector(4, seed=42).data
target_unitary_7 = np.zeros((4, 4), dtype=complex)
target_unitary_7[:, 0] = target_state
q, r = np.linalg.qr(target_unitary_7)
target_unitary_7 = q

epsilon = mpmath.mpf("0.5")
qc=QuantumCircuit(2)

qc.cx(0,1)
qc.cx(1,0)


qc.h(0)
rzgates1= gridsynth_gates(theta=0.927, epsilon=epsilon)
apply_gridsynth_gates(qc,rzgates1,0)
qc.h(0)
qc.h(1)
rzgates2= gridsynth_gates(theta=1.9263, epsilon=epsilon)
apply_gridsynth_gates(qc,rzgates2,1)
qc.h(1)
qc.cx(0,1)
qc.h(1)
rzgates3= gridsynth_gates(theta=1.0916, epsilon=epsilon)
apply_gridsynth_gates(qc,rzgates3,1)
qc.h(1)
qc.s(1)

qc.cx(1,0)
qc.cx(0,1)

dist, t_count = get_metrics(qc, target_unitary_7)
print(dist,t_count)

with open("/Users/mdsohelmondal/compilation/outputs/random_state_prep.qasm", "w") as f:
    qasm3.dump(qc, f)

# Ensure the variable name (file) matches the one used inside the block
with open("/Users/mdsohelmondal/compilation/results/random_state_prep.txt", "w") as file:
    file.write(f"Distance Norm: {dist}, T-count: {t_count}")

qc.draw(output='mpl', filename="/Users/mdsohelmondal/compilation/circuits/random_state_prep.pdf")