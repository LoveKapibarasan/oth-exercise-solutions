import numpy as np

# 1. Define base components
h_val = 1.0 / np.sqrt(2.0)
H = h_val * np.array([[1, 1], 
                      [1, -1]])
I = np.eye(2)

# CNOT 1->2 (Control: Top, Target: Bottom)
CNOT_12 = np.array([[1, 0, 0, 0],
                    [0, 1, 0, 0],
                    [0, 0, 0, 1],
                    [0, 0, 1, 0]])

# CNOT 2->1 (Control: Bottom, Target: Top)
CNOT_21 = np.array([[1, 0, 0, 0],
                    [0, 0, 0, 1],
                    [0, 0, 1, 0],
                    [0, 1, 0, 0]])

# === 2. Circuit A calculation ===
# Step 1: H ⊗ H
M_A1 = np.kron(H, H)
# Step 2: CNOT_12
M_A2 = CNOT_12
# Step 3: H ⊗ I
M_A3 = np.kron(H, I)

MA = M_A3 @ M_A2 @ M_A1

# === 3. Circuit B calculation ===
# Step 1: CNOT_21
M_B1 = CNOT_21
# Step 2: I ⊗ H
M_B2 = np.kron(I, H)

MB = M_B2 @ M_B1

# 4. Results
print("--- Matrix MA ---")
print(np.round(MA, 5))

print("\n--- Matrix MB ---")
print(np.round(MB, 5))

# Check equality using a tolerance for floating point numbers
is_equal = np.allclose(MA, MB)
print(f"\nDoes MA equal MB?: {is_equal}")

# Multiply sqrt(2)
print("\nMA multiplied by sqrt(2) (to see raw integers):")
print(np.round(MA * np.sqrt(2), 2))