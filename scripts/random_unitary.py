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
target_unitary_10 = np.array([
    [ 0.1448081895 + 0.1752383997j,
     -0.5189281551 - 0.5242425896j,
     -0.1495585824 + 0.3127549990j,
      0.1691348143 - 0.5053863118j],

    [-0.9271743926 - 0.0878506193j,
     -0.1126033063 - 0.1818584963j,
      0.1225587186 + 0.0964028611j,
     -0.2449850904 - 0.0504584131j],

    [-0.0079842758 - 0.2035507051j,
     -0.3893205530 - 0.0518092515j,
      0.2605170566 + 0.3286402481j,
      0.4451730754 + 0.6558933250j],

    [ 0.0313792249 + 0.1961395216j,
      0.4980474972 + 0.0884604926j,
      0.3407886532 + 0.7506609982j,
      0.0146480652 - 0.1575584270j]
], dtype=complex)

epsilon = mpmath.mpf("0.5")
qc=QuantumCircuit(2)
qc.cx(0,1)
qc.cx(1,0)


rzgates= gridsynth_gates(theta=-2.4189, epsilon=epsilon)
apply_gridsynth_gates(qc,rzgates,0)

#Ry~~~~~~~~~~~~~~~~~~~
theta = 1.137
epsilon = mpmath.mpf("0.5")
gates1 = gridsynth_gates(theta=theta, epsilon=epsilon)
gates2 = gridsynth_gates(theta=-1*theta, epsilon=epsilon)
#print(gates1)
qc.h(1)
qc.s(1)
apply_gridsynth_gates(qc, gates1, 0)
qc.sdg(1)
qc.h(1)
qc.cx(0,1)
qc.h(1)
qc.s(1)
apply_gridsynth_gates(qc, gates2, 0)
qc.sdg(1)
qc.h(1)
qc.cx(0,1)
#~~~~~~~~~~~~~~~~~~~~
rzgates= gridsynth_gates(theta=0.3928, epsilon=epsilon)
apply_gridsynth_gates(qc,rzgates,0)


rzgates= gridsynth_gates(theta=1.972, epsilon=epsilon)
apply_gridsynth_gates(qc,rzgates,0)
#Ry~~~~~~~~~~~~~~~~~~~
theta = 0.8469
epsilon = mpmath.mpf("0.5")
gates1 = gridsynth_gates(theta=theta, epsilon=epsilon)
gates2 = gridsynth_gates(theta=-1*theta, epsilon=epsilon)
#print(gates1)
qc.h(1)
qc.s(1)
apply_gridsynth_gates(qc, gates1, 0)
qc.sdg(1)
qc.h(1)
qc.cx(0,1)
qc.h(1)
qc.s(1)
apply_gridsynth_gates(qc, gates2, 0)
qc.sdg(1)
qc.h(1)
qc.cx(0,1)
#~~~~~~~~~~~~~~~~~~~~
rzgates= gridsynth_gates(theta=-1.2275, epsilon=epsilon)
apply_gridsynth_gates(qc,rzgates,0)

qc.h(0)
qc.h(1)
qc.cx(0,1)
rzgates= gridsynth_gates(theta=0.7227, epsilon=epsilon)
apply_gridsynth_gates(qc,rzgates,1)

qc.cx(0,1)
qc.h(0)
qc.h(1)

qc.sdg(0)
qc.h(0)
qc.sdg(1)
qc.h(1)

qc.cx(0, 1)
rzgates= gridsynth_gates(theta=0.429746, epsilon=epsilon)
apply_gridsynth_gates(qc,rzgates,1)
qc.cx(0, 1)

qc.h(0)
qc.s(0)
qc.h(1)
qc.s(1)
qc.cx(0, 1)
rzgates= gridsynth_gates(theta=0.143104, epsilon=epsilon)
apply_gridsynth_gates(qc,rzgates,1)
qc.cx(0, 1)
rzgates= gridsynth_gates(theta=-0.73488, epsilon=epsilon)
apply_gridsynth_gates(qc,rzgates,0)

#Ry~~~~~~~~~~~~~~~~~~~
theta = 1.55241
epsilon = mpmath.mpf("0.5")
gates1 = gridsynth_gates(theta=theta, epsilon=epsilon)
gates2 = gridsynth_gates(theta=-1*theta, epsilon=epsilon)
#print(gates1)
qc.h(1)
qc.s(1)
apply_gridsynth_gates(qc, gates1, 0)
qc.sdg(1)
qc.h(1)
qc.cx(0,1)
qc.h(1)
qc.s(1)
apply_gridsynth_gates(qc, gates2, 0)
qc.sdg(1)
qc.h(1)
qc.cx(0,1)
#~~~~~~~~~~~~~~~~~~
#rzgates= gridsynth_gates(theta=2.19476, epsilon=epsilon)
#apply_gridsynth_gates(qc,rzgates,0)

qc.cx(1,0)
qc.cx(0,1)
dist, t_count = get_metrics(qc, target_unitary_10)
print(dist,t_count)

with open("/Users/mdsohelmondal/compilation/outputs/random_unitary.qasm", "w") as f:
    qasm3.dump(qc, f)

# Ensure the variable name (file) matches the one used inside the block
with open("/Users/mdsohelmondal/compilation/results/random_unitary.txt", "w") as file:
    file.write(f"Distance Norm: {dist}, T-count: {t_count}")

qc.draw(output='mpl', filename="/Users/mdsohelmondal/compilation/circuits/random_unitary.pdf")