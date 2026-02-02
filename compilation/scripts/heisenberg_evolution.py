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

# Target Unitary exp(i * theta * XX+YY+ZZ) (Heisenberg Evolution)
phase = np.exp(1j * np.pi / 4)

target_unitary_5 = np.array([
    [1, 0, 0, 0],
    [0, 0, 1, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 1]
])

qc=QuantumCircuit(2)

#qc.cx(0,1)
#qc.cx(1,0)


qc.cx(0,1)
qc.cx(1,0)
qc.cx(0,1)

#qc.cx(1,0)
#qc.cx(0,1)

dist, t_count = get_metrics(qc, target_unitary_5)
print(dist,t_count)

with open("/Users/mdsohelmondal/compilation/outputs/heisenberg_evolution.qasm", "w") as f:
    qasm3.dump(qc, f)

# Ensure the variable name (file) matches the one used inside the block
with open("/Users/mdsohelmondal/compilation/results/heisenberg_evolution.txt", "w") as file:
    file.write(f"Distance Norm: {dist}, T-count: {t_count}")

qc.draw(output='mpl', filename="/Users/mdsohelmondal/compilation/circuits/heisenberg_evolution.pdf")