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

# Target Unitary for Phase encoded QFT on 2 qubits
QFT2 = 0.5 * np.array([
    [1, 1, 1, 1],
    [1, 1j, -1, -1j],
    [1, -1, 1, -1],
    [1, -1j, -1, 1j]
])
M2 = np.array([
    [1, 0, 0, 0],
    [0, 0, -0.5+0.5j, 0.5+0.5j],
    [0, 1j, 0, 0],
    [0, 0, -0.5-0.5j, -0.5+0.5j]
])
target_unitary_9 = QFT2 @ M2

epsilon = mpmath.mpf("0.5")
qc=QuantumCircuit(2)

qc.cx(0,1)
qc.cx(1,0)


qc.h(1)
qc.cx(1,0)
qc.sdg(0)
qc.cx(1,0)
qc.h(1)


qc.cx(1,0)
qc.cx(0,1)

dist, t_count = get_metrics(qc, target_unitary_9)
print(dist,t_count)

with open("/Users/mdsohelmondal/compilation/outputs/structured_unitary2.qasm", "w") as f:
    qasm3.dump(qc, f)

# Ensure the variable name (file) matches the one used inside the block
with open("/Users/mdsohelmondal/compilation/results/structured_unitary2.txt", "w") as file:
    file.write(f"Distance Norm: {dist}, T-count: {t_count}")

qc.draw(output='mpl', filename="/Users/mdsohelmondal/compilation/circuits/structured_unitary2.pdf")