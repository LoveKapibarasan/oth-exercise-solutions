import cirq

def twoway_OR(circuit, a, b, c, not_a, not_b):
    """
    Implements c = a OR b using the approach described in the lecture handouts.
    """
    if not_a: circuit.append(cirq.X(a))
    if not_b: circuit.append(cirq.X(b))
    
    circuit.append(cirq.CCNOT(a, b, c))
    circuit.append(cirq.CNOT(a, c))
    circuit.append(cirq.CNOT(b, c))
    
    if not_a: circuit.append(cirq.X(a))
    if not_b: circuit.append(cirq.X(b))

def threeway_OR(circuit, a, b, c, d, ancilla, not_a, not_b, not_c):
    """
    Implements d = a OR b OR c.
    Requires an ancilla qubit to store the intermediate result (a OR b).
    """
    # 1. Step: (a OR b) -> ancilla
    twoway_OR(circuit, a, b, ancilla, not_a, not_b)
    
    # 2. Step: (ancilla OR c) -> d
    twoway_OR(circuit, ancilla, c, d, 0, not_c)
    
    # 3. Clean up: Uncompute ancilla to restore its state to |0>
    # (By reversing the first twoway_OR)
    twoway_OR(circuit, a, b, ancilla, not_a, not_b)

    return circuit

def unoptimized_oracle(qubits):
    """
    Constructs the unoptimized oracle for the Alexandria Ship problem.
    """
    circuit = cirq.Circuit()
    
    # 1. ¬A ∨ ¬C
    twoway_OR(circuit, qubits[0], qubits[1], qubits[4], 1, 1)
    # 2. ¬A ∨ J ∨ P
    threeway_OR(circuit, qubits[0], qubits[2], qubits[3], qubits[6], qubits[5], 1, 0, 0)
    
    # 3. ¬P ∨ J
    twoway_OR(circuit, qubits[3], qubits[2], qubits[7], 1, 0)
    # 4. ¬P ∨ ¬C
    twoway_OR(circuit, qubits[3], qubits[1], qubits[8], 1, 1)
    # 5. J
    circuit.append(cirq.CNOT(qubits[2], qubits[9]))
    # 6. ¬C ∨ ¬J
    twoway_OR(circuit, qubits[1], qubits[2], qubits[10], 1, 1)
    
    # Final Phase Flip (Marking the solution)
    circuit.append(cirq.X(qubits[11]).controlled_by(*qubits[4:11]))
    
    return circuit

def diffusion_operator(qubits):
    """
    Inversion about the mean: H -> X -> Multi-Controlled Z -> X -> H
    """
    circuit = cirq.Circuit()
    circuit.append([cirq.H(q) for q in qubits[:4]])
    circuit.append([cirq.X(q) for q in qubits[:4]])
    # Multi-controlled Z gate on input qubits
    circuit.append(cirq.Z(qubits[3]).controlled_by(*qubits[:3]))
    circuit.append([cirq.X(q) for q in qubits[:4]])
    circuit.append([cirq.H(q) for q in qubits[:4]])
    return circuit

def main():
    # Setup qubits: [A, C, J, P] (0-3) + Ancilla (4-10) + Target (11)
    qubits = cirq.LineQubit.range(12)
    circuit = cirq.Circuit()
    
    # 1. Initialize |s> and Target |->
    circuit.append([cirq.H(q) for q in qubits[:4]])
    circuit.append([cirq.X(qubits[11]), cirq.H(qubits[11])])
    
    # 2. Grover Iteration (Run oracle and diffusion ~sqrt(2^4)=4 times)
    for _ in range(4):
        circuit.append(unoptimized_oracle(qubits))
        circuit.append(diffusion_operator(qubits))
    
    # 3. Measurement
    circuit.append(cirq.measure(*qubits[:4], key='result'))
    
    # 4. Simulation
    result = cirq.Simulator().run(circuit, repetitions=8192)
    print("Measurement Histogram:")
    print(result.histogram(key='result'))

if __name__ == "__main__":
    main()