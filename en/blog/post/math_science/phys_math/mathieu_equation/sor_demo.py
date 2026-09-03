import numpy as np
import matplotlib.pyplot as plt

def sor_hyperbolic_electrodes(n=100):
    # Set up the array
    v = np.zeros((n, n))
    u = np.zeros((n, n))
    
    ok = 0.0001
    max_diff = 0.002
    w = 1.93908
    
    # Set hyperbolic conditions
    scale = n / 100  # Scale factor for 100x100 to nxn
    center = n // 2
    
    # Upper and Lower
    for j in range(n):
        x = (j - center) / scale
        if abs(x) <= 25:
            y = np.sqrt(100 + 2.4 * x**2)
            i_upper = int(center + y * scale)
            i_lower = int(center - y * scale)
            
            for i in [i_upper, i_lower]:
                if 0 <= i < n:
                    for di in [-1, 0, 1]:
                        for dj in [-1, 0, 1]:
                            if 0 <= i+di < n and 0 <= j+dj < n:
                                v[i+di, j+dj] = u[i+di, j+dj] = 1.0
    
    # Left and Right
    for i in range(n):
        y = (i - center) / scale
        if abs(y) <= 25:
            x = np.sqrt(100 + 2.4 * y**2)
            j_left = int(center + x * scale)
            j_right = int(center - x * scale)
            
            for j in [j_left, j_right]:
                if 0 <= j < n:
                    for di in [-1, 0, 1]:
                        for dj in [-1, 0, 1]:
                            if 0 <= i+di < n and 0 <= j+dj < n:
                                v[i+di, j+dj] = u[i+di, j+dj] = -1.0
    
    # SOR Method
    count = 0
    while max_diff > ok and count < 10000:  # Added iteration limit
        max_diff = ok
        count += 1
        
        for i in range(1, n-1):
            for j in range(1, n-1):
                if -1 < v[i, j] < 1:
                    alpha = 0.25 * (v[i+1, j] + u[i-1, j] + v[i, j+1] + u[i, j-1])
                    u[i, j] = v[i, j] + w * (alpha - v[i, j])
                    u[i, j] = np.clip(u[i, j], -1, 1)
                    
                    diff = abs(v[i, j] - u[i, j])
                    if diff > max_diff:
                        max_diff = diff
        
        v = u.copy()
        
        if count % 100 == 0:
            print(f"Iteration {count}, max difference: {max_diff}")
    
    print(f"SOR took {count} iterations.")
    return v

# Run the SOR method
n = 1000  # You can change this to any value
potential = sor_hyperbolic_electrodes(n)

# Plotting
plt.figure(figsize=(12, 10))
im = plt.imshow(potential, cmap='viridis', extent=[0, n, 0, n], origin='lower')
plt.colorbar(im, label='Potential')
plt.title(f'Potential Distribution for Hyperbolic Electrodes (Grid Size: {n}x{n})')
plt.xlabel('X')
plt.ylabel('Y')
plt.show()