import numpy as np
import matplotlib.pyplot as plt

def calculate_stability(q_range, a_range):
    pi = np.pi
    e = np.zeros(250)  # Increased size to 250
    d = np.zeros(101)
    
    results = []
    
    for q in q_range:
        for a in a_range:
            # Set all components
            m_values = np.arange(0, 249, 2)
            e[m_values] = q / ((m_values ** 2) - a)
            
            # The first seed determinants, from Maple worksheet
            d[3] = (-2*e[2]**2*e[0]*e[4]**2*e[6] + e[2]**2*e[4]**2 - 2*e[4]**2*e[2]*e[0]*e[6]**2 
                    + 2*e[2]*e[4]**2*e[6] + e[4]**2*e[6]**2 + 2*e[2]**2*e[0]*e[4] 
                    + 4*e[2]*e[0]*e[6]*e[4] - 2*e[2]*e[4] - 2*e[6]*e[4] - 2*e[2]*e[0] + 1)
            d[2] = 1 - 2*e[2]*e[4] - 2*e[2]*e[0] + 2*e[2]**2*e[0]*e[4] + e[2]**2*e[4]**2
            d[1] = 1 - 2*e[2]*e[0]
            d[0] = 1
            
            # Here goes Strang's iteration method
            for m in range(4, 101):
                alpha = e[2*m] * e[2*(m-1)]
                beta = 1 - alpha
                alpha1 = e[2*(m-1)] * e[2*(m-2)]
                d[m] = beta * d[m-1] - alpha * beta * d[m-2] + alpha * alpha1**2 * d[m-3]
            
            # Find mu, make separate case for -a situation
            if a >= 0:
                mu = np.arccos(1 - (d[100]) * (1 - np.cos(pi * np.sqrt(a)))) / pi
            else:
                mu = np.arccos(1 - (d[100]) * (1 - np.cosh(pi * np.sqrt(abs(a))))) / pi
            
            # If mu is nan then make it zero
            if np.isnan(mu):
                mu = 0.0
            
            results.append((q, a, mu))
            
            # Reflect across a = 0, retaining the original mu
            if a != 0:
                results.append((q, -a, mu))
    
    return results

def plot_stability(results):
    q_values, a_values, mu_values = zip(*results)
    
    plt.figure(figsize=(10, 8))
    plt.scatter(q_values, a_values, c=mu_values, cmap='viridis', s=1)
    plt.colorbar(label='μ')
    plt.xlabel('q')
    plt.ylabel('a')
    plt.title("Stability Diagram for Mathieu's Equation")
    plt.savefig('mathieu_stability_diagram_rf_zoom.png')
    #plt.show()

# Define the range for q and a
q_range = np.arange(-2.5, 2.5, 0.005)
a_range = np.arange(-3, 3, 0.0175)

# Calculate stability
results = calculate_stability(q_range, a_range)

# Plot the results
plot_stability(results)
