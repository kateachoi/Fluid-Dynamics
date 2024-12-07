import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import PillowWriter, FuncAnimation
from PIL import Image
import noise

# Load the background image
background_path = '/Users/katechoi/aurora/.venv/sky.png'  # Replace with your background path
background = Image.open(background_path)
background_array = np.array(background)

# Aurora simulation parameters
x = np.linspace(0, 2 * np.pi, 800)
y = np.linspace(0, 2 * np.pi, 300)
X, Y = np.meshgrid(x, y)


# Function to generate aurora-like waves using Perlin noise
def aurora_wave(t):
    noise_grid = np.zeros_like(X)
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            noise_grid[i, j] = noise.pnoise2(X[i, j] + t * 0.1, Y[i, j] + t * 0.1, octaves=4, persistence=0.5,
                                             lacunarity=2.0)

    return noise_grid


# Prepare the figure and axis
fig, ax = plt.subplots(figsize=(10, 6), dpi=150)
ax.axis("off")

# Overlay the background
ax.imshow(background_array, extent=[0, 2 * np.pi, 0, 2 * np.pi], aspect='auto')

# Initialize the aurora effect with Perlin noise
aurora = ax.imshow(
    np.zeros_like(X),
    extent=[0, 2 * np.pi, 0, 2 * np.pi],
    cmap='plasma',  # Color map can be changed to 'plasma' or any desired color map
    alpha=0.6,
    aspect='auto'
)

# Add colorbar (legend for the aurora intensity)
cbar = fig.colorbar(aurora, ax=ax, orientation="vertical")
cbar.set_label('Aurora Intensity')


# Update function for animation using Perlin noise
def update(frame):
    wave = aurora_wave(frame)
    aurora.set_data(wave)
    aurora.set_clim(vmin=-1, vmax=1)  # Normalize intensity
    return [aurora]


# Create animation
ani = FuncAnimation(fig, update, frames=200, interval=100, blit=True)

# Save animation as GIF using PillowWriter
output_path = "/Users/katechoi/aurora/.venv/perlin.gif"
writer = PillowWriter(fps=10)
ani.save(output_path, writer=writer)

plt.close(fig)
print(f"Aurora simulation with Perlin noise saved as {output_path}")
