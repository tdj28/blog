import sympy as sp

def calculate_mathieu_determinants():
    # Define symbolic variables
    e0, e2, e4, e6 = sp.symbols('e0 e2 e4 e6')

    # Define matrices
    C = sp.Matrix([
        [1, e6, 0, 0, 0, 0, 0],
        [e4, 1, e4, 0, 0, 0, 0],
        [0, e2, 1, e2, 0, 0, 0],
        [0, 0, e0, 1, e0, 0, 0],
        [0, 0, 0, e2, 1, e2, 0],
        [0, 0, 0, 0, e4, 1, e4],
        [0, 0, 0, 0, 0, e6, 1]
    ])

    A = sp.Matrix([
        [1, e4, 0, 0, 0],
        [e2, 1, e2, 0, 0],
        [0, e0, 1, e0, 0],
        [0, 0, e2, 1, e2],
        [0, 0, 0, e4, 1]
    ])

    B = sp.Matrix([
        [1, e2, 0],
        [e0, 1, e0],
        [0, e2, 1]
    ])

    # Calculate determinants
    det_C = C.det()
    det_A = A.det()
    det_B = B.det()

    # Simplify the expressions
    det_C = sp.simplify(det_C)
    det_A = sp.simplify(det_A)
    det_B = sp.simplify(det_B)

    return det_C, det_A, det_B

# Calculate the determinants
d3, d2, d1 = calculate_mathieu_determinants()

# Print the results
print("d[3] =", d3)
print("d[2] =", d2)
print("d[1] =", d1)
print("d[0] = 1")  # This is always 1 by definition
