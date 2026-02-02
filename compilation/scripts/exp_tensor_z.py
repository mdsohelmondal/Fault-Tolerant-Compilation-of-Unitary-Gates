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

# Target Unitary exp(i * pi/7 * ZZ)
target_unitary3 = np.array([
    [np.exp(1j*np.pi/7), 0, 0, 0],
    [0, np.exp(-1j*np.pi/7), 0, 0],
    [0, 0, np.exp(-1j*np.pi/7), 0],
    [0, 0, 0, np.exp(1j*np.pi/7)]
])

epsilon = mpmath.mpf("0.5")
qc=QuantumCircuit(2)

qc.cx(0,1)
rzgates= gridsynth_gates(theta=2*np.pi/7, epsilon=epsilon)
apply_gridsynth_gates(qc,rzgates,1)
qc.cx(0,1)

dist, t_count = get_metrics(qc, target_unitary3)
print(dist,t_count)

with open("/Users/mdsohelmondal/compilation/outputs/exp_tensor_z.qasm", "w") as f:
    qasm3.dump(qc, f)

# Ensure the variable name (file) matches the one used inside the block
with open("/Users/mdsohelmondal/compilation/results/exp_tensor_z.txt", "w") as file:
    file.write(f"Distance Norm: {dist}, T-count: {t_count}")

qc.draw(output='mpl', filename="/Users/mdsohelmondal/compilation/circuits/exp_tensor_z.pdf")