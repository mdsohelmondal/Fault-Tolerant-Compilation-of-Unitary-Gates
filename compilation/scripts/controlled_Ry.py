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

# Target Unitary for Controlled-RY(pi/7)
target_unitary2 = np.array([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 0.97492791, -0.22252093],
    [0, 0, 0.22252093,  0.97492791]
])

theta = mpmath.mp.pi/14
epsilon = mpmath.mpf("0.5")
gates1 = gridsynth_gates(theta=theta, epsilon=epsilon)
gates2 = gridsynth_gates(theta=-1*theta, epsilon=epsilon)

qc=QuantumCircuit(2)

qc.cx(0,1)
qc.cx(1,0)

qc.h(1)
qc.s(1)
apply_gridsynth_gates(qc, gates1, 1)
qc.sdg(1)
qc.h(1)
qc.cx(0,1)
qc.h(1)
qc.s(1)
apply_gridsynth_gates(qc, gates2, 1)
qc.sdg(1)
qc.h(1)
qc.cx(0,1)

qc.cx(1,0)
qc.cx(0,1)

dist, t_count = get_metrics(qc, target_unitary2)

with open("/Users/mdsohelmondal/compilation/outputs/controlled_ry.qasm", "w") as f:
    qasm3.dump(qc, f)

# Ensure the variable name (file) matches the one used inside the block
with open("/Users/mdsohelmondal/compilation/results/controlled_ry.txt", "w") as file:
    file.write(f"Distance Norm: {dist}, T-count: {t_count}")

qc.draw(output='mpl', filename="/Users/mdsohelmondal/compilation/circuits/controlled_ry.pdf")