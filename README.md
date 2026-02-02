# Fault-Tolerant Compilation of Unitary Gates

This repository presents the fault-tolerant compilation of several useful quantum unitary gates using the **Clifford+T gate set**. The project was developed as part of a challenge proposed by **Superquantum** at the **MIT Quantum Hackathon (iQuHack) 2026**.

The objective is to approximate target unitary operations with high fidelity while minimizing costly non-Clifford resources, which are critical in fault-tolerant quantum computing.

---

## Problem Statement

In fault-tolerant quantum computing, quantum circuits must be expressed using a discrete, error-correctable gate set. Clifford gates are efficiently implementable under quantum error correction, but they are not universal. Universality is achieved by introducing **T gates**, which significantly increase resource overhead.

The challenge addressed in this project is to:

- **Minimize the number of T gates (T-count)** used in the circuit  
- **Minimize the operator norm distance** between the target unitary and the compiled approximation  

These two objectives often compete, making circuit compilation a non-trivial optimization problem.

---

## Approach

For a given target unitary, we:

- Construct quantum circuits using only **Clifford and T gates**
- Evaluate circuit performance using:
  - **T-count** as a measure of fault-tolerant resource cost
  - **Operator norm distance** as a measure of approximation accuracy
- Benchmark multiple candidate circuits to explore trade-offs between accuracy and resource efficiency

All simulations and evaluations are implemented in **Python** using **Qiskit**.

---

## Key Features

- Clifford+T decompositions of commonly used unitary gates  
- Explicit optimization of T-count for fault-tolerant execution  
- Quantitative benchmarking using operator norm distance  
- Reproducible simulation and evaluation workflow  

---

## Repository Structure

```text
.
├── scripts/        # Source code for compiled Clifford+T circuits
├── outputs/        # Generated circuit files in .qasm format
├── circuits/       # PDF visualizations of the compiled circuits
├── results/        # T-gate counts and operator norm distance metrics
├── challenge.pdf   # Original challenge description by Superquantum (iQuHack 2026)
├── LICENSE         # License information
└── README.md
