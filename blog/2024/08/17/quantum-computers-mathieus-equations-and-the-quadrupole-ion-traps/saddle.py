import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Create a figure for plotting
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Define the hyperbolic surface
x = np.linspace(-1, 1, 100)
y = np.linspace(-1, 1, 100)
x, y = np.meshgrid(x, y)
z = x**2 - y**2

# Plot the hyperbolic surface
ax.plot_wireframe(x, y, z, color='cyan', alpha=0.6)

# Position the ball directly on the saddle surface
ball_x = 0.5
ball_y = 0.3
ball_z = ball_x**2 - ball_y**2 + 0.0

# Draw a ball using plot_surface for a more realistic representation
u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
ball_x_sphere = 0.1*np.cos(u)*np.sin(v)
ball_y_sphere = 0.1*np.sin(u)*np.sin(v)
ball_z_sphere = 0.1*np.cos(v) + ball_z + 0.05  # Slightly raise the ball above the surface

ax.plot_surface(ball_x_sphere, ball_y_sphere, ball_z_sphere, color='red')

# Adjust the view to rotate by 90 degrees
ax.view_init(elev=20, azim=120)

# Remove the grid box and axis
ax.grid(False)
ax.axis('off')

# Show the plot
plt.show()
