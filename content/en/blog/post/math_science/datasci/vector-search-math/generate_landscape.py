import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

# Generate data
x = np.linspace(-6, 6, 100)
y = np.linspace(-6, 6, 100)
X, Y = np.meshgrid(x, y)

# Global Minimum at (0,0) approx, surrounded by local minima
# Function: z = x^2/10 + y^2/10 + cos(x) + cos(y)
Z = (X**2)/5 + (Y**2)/5 + 2*np.cos(X) + 2*np.cos(Y)

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Plot surface with transparency
surf = ax.plot_surface(X, Y, Z, cmap=cm.viridis, alpha=0.9, antialiased=True)

# Annotate Peaks and Valleys
# We want to show a "False Minimum" (Local) vs "True Minimum" (Global)

# Global min is roughly at (0,0)? Actually cos(0)=1, so 0+0+2+2=4.
# Let's check min value. cos(pi)=-1. at x=pi, z = pi^2/10 - 1. 
# Let's just find min programmatically to identify points.

min_idx = np.unravel_index(np.argmin(Z, axis=None), Z.shape)
global_min_x, global_min_y, global_min_z = X[min_idx], Y[min_idx], Z[min_idx]

# Find a local minimum (a false peak/valley)
# We can just pick a spot that looks like a valley but isn't the deepest.
# (3, 3) approx?
# Let's manually pick convenient points for illustration logic.
# "Start" point (high up)
start_x, start_y = -5, -5
start_z = (start_x**2)/5 + (start_y**2)/5 + 2*np.cos(start_x) + 2*np.cos(start_y)

# "False Minimum" (Local)
local_x, local_y = 3.2, 3.2
local_z = (local_x**2)/5 + (local_y**2)/5 + 2*np.cos(local_x) + 2*np.cos(local_y)

# True Minimum (Global) - roughly closest to (0,0) in the valley?
# Actually with x^2/10 + cos(x), the global min is slightly offset from 0 if the quadratic term is weak.
# But (0,0) is a local max because cos''(0) = -1 < 0.
# The valleys are around pi.
# x=pi (~3.14). z = 3.14^2/5 - 2 = 1.96 - 2 = -0.04.
# x=0. z = 4.
# So (pi, pi) is a deep valley?
# Let's simply label the Deepest point found as "Global Minimum"
# And a higher valley as "Local Minimum".

ax.scatter([global_min_x], [global_min_y], [global_min_z], color='red', s=100, label='Global Minimum (True Target)')

# Let's find a local min that is clearly higher than global min
# Scan for a local min in the grid?
from scipy.signal import argrelextrema
# Or just visual approximation: around (-3, 3)
false_x, false_y = -3.2, 3.2
false_z = (false_x**2)/5 + (false_y**2)/5 + 2*np.cos(false_x) + 2*np.cos(false_y)
ax.scatter([false_x], [false_y], [false_z], color='orange', s=100, label='Local Minimum (False Peak)')

start_path_x, start_path_y = -4, 4
start_path_z = (start_path_x**2)/5 + (start_path_y**2)/5 + 2*np.cos(start_path_x) + 2*np.cos(start_path_y)
ax.scatter([start_path_x], [start_path_y], [start_path_z], color='green', s=100, label='Greedy Start Point')

# Draw arrows?
# Greedy Path: Start -> Local Min
ax.plot([start_path_x, false_x], [start_path_y, false_y], [start_path_z, false_z], color='black', linestyle='--', linewidth=2, label='Greedy Path (Stuck)')

# Beam Path: Start -> ... -> Global Min
# Just conceptually show it crossing the ridge
ax.plot([start_path_x, 0, global_min_x], [start_path_y, 0, global_min_y], [start_path_z, 2, global_min_z], color='blue', linestyle='-', linewidth=2, label='Beam Search (Explores)')

ax.set_title('Optimization Landscape: Local vs Global Minima')
ax.legend()
plt.savefig('/data2/blog/content/en/blog/post/math_science/datasci/vector-search-math/local_vs_global.png')
print("Image saved to /data2/blog/content/en/blog/post/math_science/datasci/vector-search-math/local_vs_global.png")
