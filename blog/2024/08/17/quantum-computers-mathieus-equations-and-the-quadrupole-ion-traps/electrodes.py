import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.animation as animation
from tqdm import tqdm
import imageio

def sor_hyperbolic_electrodes(n, t, frequency):
    v = np.zeros((n, n), dtype=np.float64)
    u = np.zeros((n, n), dtype=np.float64)
    
    ok = 0.0001
    max_diff = 0.002
    w = 1.93908
    
    scale = n / 100
    center = n // 2
    
    # Calculate the voltage for this time step
    voltage_upper_lower = np.sin(2 * np.pi * frequency * t)
    voltage_left_right = -np.sin(2 * np.pi * frequency * t)
    
    # Set hyperbolic conditions
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
                                v[i+di, j+dj] = u[i+di, j+dj] = voltage_upper_lower
    
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
                                v[i+di, j+dj] = u[i+di, j+dj] = voltage_left_right
    
    # SOR Method
    count = 0
    while max_diff > ok and count < 100:  # Reduced iteration limit for speed
        max_diff = ok
        count += 1
        
        for i in range(1, n-1):
            for j in range(1, n-1):
                if abs(v[i, j]) < 1:
                    alpha = 0.25 * (v[i+1, j] + u[i-1, j] + v[i, j+1] + u[i, j-1])
                    u[i, j] = v[i, j] + w * (alpha - v[i, j])
                    u[i, j] = np.clip(u[i, j], -1, 1)
                    
                    diff = abs(v[i, j] - u[i, j])
                    if diff > max_diff:
                        max_diff = diff
        
        v = u.copy()
    
    return v

def calculate_electric_field(potential, n):
    Ey, Ex = np.gradient(-potential)
    E = np.sqrt(Ex**2 + Ey**2)
    Ex_normalized = Ex / (E + 1e-10)  # Add small value to avoid division by zero
    Ey_normalized = Ey / (E + 1e-10)
    return Ex_normalized, Ey_normalized, E

def animate_electrodes(n=100, duration=1, fps=30, frequency=0.5, arrow_density=10):
    fig, ax = plt.subplots(figsize=(10, 8), dpi=100)
    
    potential = sor_hyperbolic_electrodes(n, 0, frequency)
    
    # Debug information
    print(f"Potential shape: {potential.shape}")
    print(f"Potential dtype: {potential.dtype}")
    print(f"Potential min: {np.min(potential)}, max: {np.max(potential)}")
    
    im = ax.imshow(potential, cmap='viridis', animated=True, extent=[0, n, 0, n], origin='lower')
    
    plt.colorbar(im, label='Potential')
    ax.set_title(f'Potential Distribution (Grid Size: {n}x{n})')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    
    Ex, Ey, E = calculate_electric_field(potential, n)
    
    X, Y = np.meshgrid(np.arange(0, n, arrow_density), np.arange(0, n, arrow_density))
    quiver = ax.quiver(X, Y, Ex[::arrow_density, ::arrow_density], Ey[::arrow_density, ::arrow_density], 
                       E[::arrow_density, ::arrow_density], cmap='coolwarm', scale=50, pivot='mid')
    
    total_frames = int(duration * fps)
    
    pbar = tqdm(total=total_frames, desc="Generating frames", unit="frame")
    
    def update(frame):
        t = frame / fps
        potential = sor_hyperbolic_electrodes(n, t, frequency)
        im.set_array(potential)
        
        Ex, Ey, E = calculate_electric_field(potential, n)
        quiver.set_UVC(Ex[::arrow_density, ::arrow_density], Ey[::arrow_density, ::arrow_density], 
                       E[::arrow_density, ::arrow_density])
        
        ax.set_title(f'Potential Distribution at t={t:.2f}s')
        pbar.update(1)
        
        return [im, quiver]
    
    anim = FuncAnimation(fig, update, frames=total_frames, interval=1000/fps, blit=True)
    
    print("\nSaving animation as MP4...")
    writer = animation.FFMpegWriter(fps=fps, metadata=dict(artist='Me'), bitrate=1800)
    anim.save('hyperbolic_electrodes_with_field.mp4', writer=writer)
    print("Animation saved as 'hyperbolic_electrodes_with_field.mp4'")
    
    pbar.close()
    plt.close(fig)

# Example usage
print("Starting animation creation...")
animate_electrodes(n=300, duration=2, fps=30, frequency=0.5, arrow_density=10)
print("Animation process completed.")