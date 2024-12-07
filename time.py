import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# define magnetic latitude (MLAT) and local time (MLT) grid
mlat = np.linspace(50, 90, 300)  # magnetic latitude (º)
mlt = np.linspace(0, 24, 400)  # magnetic local time (hrs)
MLAT, MLT = np.meshgrid(mlat, mlt)

# convert MLT to radians for polar plotting
theta = 2 * np.pi * MLT / 24

# aurora intensity distribution (base Gaussian model)
def aurora_intensity(MLAT, peak_mlat=70, width=3, peak_intensity=1):
    """Gaussian intensity distribution centered at peak_mlat."""
    intensity = peak_intensity * np.exp(-((MLAT - peak_mlat)**2) / (2 * width**2))
    return intensity

# magnetic disturbances (time-dependent modulation term)
def magnetic_disturbance(MLAT, theta, t, amp=0.3, freq=3):
    """Time-dependent sinusoidal magnetic disturbance."""
    return amp * np.sin(freq * theta + 0.1 * t) * np.exp(-((MLAT - 70)**2) / 20)

# particle trajectories (simulated as spirals
def particle_trajectory(N, t):
    """Simulates particle trajectories spiraling along magnetic field lines."""
    # spiral motion parameters
    omega = 0.2
    mlat_particles = 70 + 5 * np.sin(omega * t + np.linspace(0, 2 * np.pi, N))
    mlt_particles = (np.linspace(0, 24, N) + 0.1 * t) % 24  # wrap around MLT
    theta_particles = 2 * np.pi * mlt_particles / 24

    return theta_particles, mlat_particles

# set up figure and polar axis
fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(10, 10))
cmap = plt.get_cmap('plasma')

# initialize particle scatter plot
N = 20
theta_particles, r_particles = particle_trajectory(N, 0)
particles = ax.scatter(theta_particles, r_particles, color='white', s=10, alpha=0.8)

intensity = aurora_intensity(MLAT)
aurora = ax.pcolormesh(theta, MLAT, intensity, shading='auto', cmap=cmap)

cbar = plt.colorbar(aurora, ax=ax, orientation='vertical', pad=0.1)
cbar.set_label('Auroral Intensity', fontsize=12)
ax.set_title("Auroral Oval Simulation", fontsize=18, pad=20)
ax.grid(True)

# update animation
def update(t):
    global particles

    # update auroral intensity with disturbances
    updated_intensity = aurora_intensity(MLAT) + magnetic_disturbance(MLAT, theta, t)
    aurora.set_array(updated_intensity.ravel())

    # update particle trajectories
    theta_particles, r_particles = particle_trajectory(N, t)
    particles.set_offsets(np.c_[theta_particles, r_particles])

    # set plot limits + title
    ax.set_rmax(90)
    ax.set_rticks([50, 60, 70, 80, 90])  # set radial ticks for magnetic latitude
    ax.set_yticklabels(['50º', '60º', '70º', '80º', '90º'], fontsize=10)
    ax.set_title(f"Auroral Oval Simulation (Time: {t:.1f} s)", fontsize=16, pad=20)

# create animation
anim = FuncAnimation(fig, update, frames=np.linspace(0, 100, 200), interval=50, blit=False)
anim.save('/Users/katechoi/Desktop/time-dependent_sim.gif', writer='pillow', fps=20)
plt.show()



