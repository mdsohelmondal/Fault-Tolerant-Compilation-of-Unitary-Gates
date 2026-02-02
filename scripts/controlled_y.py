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

# Target Unitary for Controlled-Y
target_unitary_1 = np.array([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 0, -1j],
    [0, 0, 1j, 0]
])

qc=QuantumCircuit(2)

qc.cx(0,1)
qc.cx(1,0)

qc.s(1)
qc.cx(0, 1)
qc.sdg(1)

qc.cx(1,0)
qc.cx(0,1)

dist, t_count = get_metrics(qc, target_unitary_1)
print(dist, t_count)

with open("/Users/mdsohelmondal/compilation/outputs/controlled_y.qasm", "w") as f:
    qasm3.dump(qc, f)

# Ensure the variable name (file) matches the one used inside the block
with open("/Users/mdsohelmondal/compilation/results/controlled_y.txt", "w") as file:
    file.write(f"Distance Norm: {dist}, T-count: {t_count}")

qc.draw(output='mpl', filename="/Users/mdsohelmondal/compilation/circuits/controlled_y.pdf")