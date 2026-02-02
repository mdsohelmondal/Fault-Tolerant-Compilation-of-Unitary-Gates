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

# Target Unitary for random unitary
phases = [0, np.pi, 5*np.pi/4, 7*np.pi/4, 5*np.pi/4, 7*np.pi/4, 3*np.pi/2, 3*np.pi/2, 5*np.pi/4, 7*np.pi/4, 3*np.pi/2, 3*np.pi/2, 3*np.pi/2, 3*np.pi/2, 7*np.pi/4, 5*np.pi/4]
target_unitary_11 = np.diag([np.exp(1j * p) for p in phases])


epsilon = mpmath.mpf("0.5")
qc=QuantumCircuit(4)
qc.cx(0,1)
qc.cx(1,0)


qc.s(3)
qc.t(2)
qc.t(1) 
qc.t(3)  
qc.cx(0, 1)
qc.s(1)
qc.cx(0, 1)
qc.cx(2, 3)
qc.s(3)
qc.cx(2, 3)

qc.cx(1,0)
qc.cx(0,1)

dist, t_count = get_metrics(qc, target_unitary_11)
print(dist,t_count)

with open("/Users/mdsohelmondal/compilation/outputs/diagonal_unitary.qasm", "w") as f:
    qasm3.dump(qc, f)

# Ensure the variable name (file) matches the one used inside the block
with open("/Users/mdsohelmondal/compilation/results/diagonal_unitary.txt", "w") as file:
    file.write(f"Distance Norm: {dist}, T-count: {t_count}")

qc.draw(output='mpl', filename="/Users/mdsohelmondal/compilation/circuits/diagonal_unitary.pdf")