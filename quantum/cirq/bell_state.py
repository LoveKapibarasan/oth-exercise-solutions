import cirq

q0, q1 = cirq.LineQubit.range(2)


bell_circuit = cirq.Circuit(
    cirq.H(q0),        
    cirq.CNOT(q0, q1) 
)
bell_circuit.append(cirq.measure(q0, q1, key='result'))

print("Bell Circuit:")
print(bell_circuit)

simulator = cirq.Simulator()
result = simulator.simulate(bell_circuit)

print("\nFinal state vector:")
print(result.final_state_vector)

samples = simulator.run(bell_circuit, repetitions=1024)
print("Measurement histogram:")
print(samples.histogram(key='result'))