import os
import sys
import numpy as np
import mpmath
from qiskit import QuantumCircuit
from qiskit import qasm3
from qiskit.quantum_info import Operator
from pygridsynth.gridsynth import gridsynth_gates
from qiskit import qasm3

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)
from compiler_tools import apply_gridsynth_gates, get_metrics
from scipy.linalg import expm

# Target Unitary for exp(i * pi/7 * (XX + ZI + IZ))
X = np.array([[0, 1], [1, 0]])
Z = np.array([[1, 0], [0, -1]])
I = np.eye(2)
H3 = np.kron(X, X) + np.kron(Z, I) + np.kron(I, Z)
theta = np.pi / 7
target_unitary_6 = expm(1j * theta * H3)

epsilon = mpmath.mpf("0.5")
qc=QuantumCircuit(2)

qc.cx(0,1)
qc.cx(1,0)

qc.h(0)
qc.h(1)
rzgates= gridsynth_gates(theta=2*np.pi/7, epsilon=epsilon)
apply_gridsynth_gates(qc,rzgates,0)
apply_gridsynth_gates(qc,rzgates,1)
qc.cx(0,1)
apply_gridsynth_gates(qc,rzgates,1)
qc.cx(0,1)
qc.h(0)
qc.h(1)

#qc.cx(1,0)
#qc.cx(0,1)

dist, t_count = get_metrics(qc, target_unitary_6)
print(dist,t_count)

with open("/Users/mdsohelmondal/compilation/outputs/transverse_ising_eolution.qasm", "w") as f:
    qasm3.dump(qc, f)

# Ensure the variable name (file) matches the one used inside the block
with open("/Users/mdsohelmondal/compilation/results/transverse_ising_eolution.txt", "w") as file:
    file.write(f"Distance Norm: {dist}, T-count: {t_count}")

qc.draw(output='mpl', filename="/Users/mdsohelmondal/compilation/circuits/transverse_ising_eolution.pdf")