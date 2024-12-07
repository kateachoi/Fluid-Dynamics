import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import PillowWriter, FuncAnimation
from PIL import Image

# Load the background image
background_path = '/Users/katechoi/aurora/.venv/sky.png'  # Replace with the path to your background image
background = Image.open(background_path)
background_array = np.array(background)

# Aurora simulation parameters
x = np.linspace(0, 2 * np.pi, 800)
y = np.linspace(0, 2 * np.pi, 300)
X, Y = np.meshgrid(x, y)

# Function to generate aurora-like waves
def aurora_wave(t):
    return (
        0.5 * np.sin(X * 3 + t) * np.exp(-Y / (np.pi)) +
        0.3 * np.sin(X * 6 - t * 2) * np.exp(-Y / (2 * np.pi)) +
        0.2 * np.cos(X * 2 + t * 3) * np.exp(-Y / (3 * np.pi))
    )

# Prepare the figure and axis
fig, ax = plt.subplots(figsize=(10, 6), dpi=150)
ax.axis("off")

# Overlay the background (adjusting to fit the simulation area)
ax.imshow(background_array, extent=[0, 2 * np.pi, 0, 2 * np.pi], aspect='auto')

# Initialize the aurora effect with plasma colormap for better visual blending
aurora = ax.imshow(
    np.zeros_like(Y),
    extent=[0, 2 * np.pi, 0, 2 * np.pi],
    cmap='viridis',  # Change colormap to plasma
    alpha=0.5,  # Reduced transparency for better blending
    aspect='auto'
)

# Add colorbar (legend for the aurora intensity)
cbar = fig.colorbar(aurora, ax=ax, orientation="vertical")
cbar.set_label('Aurora Intensity')

# Update function for animation
def update(frame):
    wave = aurora_wave(frame / 10)
    aurora.set_data(wave)
    aurora.set_clim(vmin=-1, vmax=1)  # Normalize intensity
    return [aurora]

# Create animation
ani = FuncAnimation(fig, update, frames=200, interval=100, blit=True)

# Save animation as GIF using PillowWriter
output_path = "/Users/katechoi/aurora/.venv/viridis.gif"
writer = PillowWriter(fps=10)
ani.save(output_path, writer=writer)

plt.close(fig)
print(f"Aurora simulation saved as {output_path}")
