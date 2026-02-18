import numpy as np
import matplotlib.pyplot as plt

def calculate_ratio(dim, num_points=1000):
    # Generate random points on unit sphere
    points = np.random.randn(num_points, dim)
    points /= np.linalg.norm(points, axis=1)[:, np.newaxis]
    
    # Calculate min/max pairwise distances
    # (Approximation: compare 1st point to all others to save time)
    diff = points[1:] - points[0]
    dists = np.linalg.norm(diff, axis=1)
    
    return np.min(dists) / np.max(dists)

dims = range(10, 3000, 50)
ratios = [calculate_ratio(d) for d in dims]

plt.figure(figsize=(10, 6))
plt.plot(dims, ratios, label='Min/Max Distance Ratio')
plt.xlabel('Dimensions')
plt.ylabel('Ratio (Min/Max)')
plt.title('Curse of Dimensionality: Loss of Contrast')
plt.grid(True)
plt.savefig('curse_of_dimensionality.png')
print("Graph saved to curse_of_dimensionality.png")
