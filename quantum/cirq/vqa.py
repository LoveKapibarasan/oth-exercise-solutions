import cirq
import numpy as np

# Define qubits
q0, q1 = cirq.LineQubit.range(2)

# Parameterized circuit
theta = np.pi / 2  # Optimal parameter
circuit = cirq.Circuit(
    cirq.ry(theta).on(q0),  # Rotation
    cirq.CNOT(q0, q1)       # Entanglement
)

# Simulate
simulator = cirq.Simulator()
result = simulator.simulate(circuit)
state = result.final_state_vector
print("Final state:", np.round(state, 3))

# Measure (8192 shots)
circuit.append(cirq.measure(q0, q1, key='result'))
samples = simulator.run(circuit, repetitions=8192)
counts = samples.histogram(key='result')
print("Counts:", counts)