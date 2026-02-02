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

# Target Unitary for exp(i * theta * (XX + YY))
theta = np.pi / 7
xy_evolution = np.array([
    [1, 0, 0, 0],
    [0, np.cos(2*theta), 1j*np.sin(2*theta), 0],
    [0, 1j*np.sin(2*theta), np.cos(2*theta), 0],
    [1, 0, 0, 1]
])

epsilon = mpmath.mpf("0.5")
qc=QuantumCircuit(2)

#qc.cx(0,1)
#qc.cx(1,0)


qc.h(0)
qc.h(1)
qc.s(0)
qc.sdg(1)
qc.cx(0,1)
rzgates= gridsynth_gates(theta=4*np.pi/7, epsilon=epsilon)
apply_gridsynth_gates(qc,rzgates,1)
qc.cx(0,1)
qc.sdg(0)
qc.s(1)
#qc.h(0)
#qc.h(1)

#qc.cx(1,0)
#qc.cx(0,1)

dist, t_count = get_metrics(qc, xy_evolution)
print(dist,t_count)

with open("/Users/mdsohelmondal/compilation/outputs/xy_evolution.qasm", "w") as f:
    qasm3.dump(qc, f)

# Ensure the variable name (file) matches the one used inside the block
with open("/Users/mdsohelmondal/compilation/results/xy_evolution.txt", "w") as file:
    file.write(f"Distance Norm: {dist}, T-count: {t_count}")

qc.draw(output='mpl', filename="/Users/mdsohelmondal/compilation/circuits/xy_evolution.pdf")