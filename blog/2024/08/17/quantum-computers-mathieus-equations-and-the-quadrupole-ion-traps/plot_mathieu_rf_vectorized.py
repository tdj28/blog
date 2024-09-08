import numpy as np
import matplotlib.pyplot as plt

def calculate_stability_vectorized(q_range, a_range):
    q, a = np.meshgrid(q_range, a_range)
    pi = np.pi
    
    m_values = np.arange(0, 249, 2)[:, np.newaxis, np.newaxis]
    e = q / (m_values**2 - a)
    
    d = np.ones((101, *q.shape))
    d[1] = 1 - 2 * e[1] * e[0]
    d[2] = 1 - 2*e[1]*e[2] - 2*e[1]*e[0] + 2*e[1]**2*e[0]*e[2] + e[1]**2*e[2]**2
    d[3] = (-2*e[1]**2*e[0]*e[2]**2*e[3] + e[1]**2*e[2]**2 - 2*e[2]**2*e[1]*e[0]*e[3]**2 
            + 2*e[1]*e[2]**2*e[3] + e[2]**2*e[3]**2 + 2*e[1]**2*e[0]*e[2] 
            + 4*e[1]*e[0]*e[3]*e[2] - 2*e[1]*e[2] - 2*e[3]*e[2] - 2*e[1]*e[0] + 1)
    
    for m in range(4, 101):
        alpha = e[m] * e[m-1]
        beta = 1 - alpha
        alpha1 = e[m-1] * e[m-2]
        d[m] = beta * d[m-1] - alpha * beta * d[m-2] + alpha * alpha1**2 * d[m-3]
    
    mu = np.where(a >= 0,
                  np.arccos(1 - d[100] * (1 - np.cos(pi * np.sqrt(np.abs(a))))) / pi,
                  np.arccos(1 - d[100] * (1 - np.cosh(pi * np.sqrt(np.abs(a))))) / pi)
    
    mu = np.nan_to_num(mu)
    
    # Create reflected a and mu
    a_reflected = -a
    mu_reflected = mu
    
    # Combine original and reflected results
    q_combined = np.concatenate([q.flatten(), q.flatten()])
    a_combined = np.concatenate([a.flatten(), a_reflected.flatten()])
    mu_combined = np.concatenate([mu.flatten(), mu_reflected.flatten()])
    
    return q_combined, a_combined, mu_combined

def plot_stability(q, a, mu):
    plt.figure(figsize=(12, 10))
    
    # Create a 2D histogram-like representation
    q_bins = np.linspace(q.min(), q.max(), 400)
    a_bins = np.linspace(a.min(), a.max(), 400)
    H, q_edges, a_edges = np.histogram2d(q, a, bins=(q_bins, a_bins), weights=mu)
    H = H.T  # Transpose H to match imshow's expected orientation
    
    # Take the maximum value in each bin
    H_max = np.zeros_like(H)
    for i in range(H.shape[0]):
        for j in range(H.shape[1]):
            mask = (q >= q_edges[j]) & (q < q_edges[j+1]) & (a >= a_edges[i]) & (a < a_edges[i+1])
            if np.any(mask):
                H_max[i, j] = np.max(mu[mask])
    
    plt.imshow(H_max, extent=[q.min(), q.max(), a.min(), a.max()], 
               aspect='auto', origin='lower', cmap='viridis')
    plt.colorbar(label='μ')
    plt.xlabel('q')
    plt.ylabel('a')
    plt.title("Stability Diagram for Mathieu's Equation")
    plt.savefig('mathieu_stability_diagram_rf_v.png', dpi=300)

# Define the range for q and a
q_range = np.linspace(-10, 10, 4000)
a_range = np.linspace(-10, 10, 4000)

# Calculate stability
q, a, mu = calculate_stability_vectorized(q_range, a_range)

# Plot the results
plot_stability(q, a, mu)