import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft2, ifft2
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# define magnetic latitude (MLAT) and local time (MLT) grid
mlat = np.linspace(50, 90, 300)  # magnetic latitude (º)
mlt = np.linspace(0, 24, 400)  # magnetic local time (hrs)
MLAT, MLT = np.meshgrid(mlat, mlt)

# convert MLT to radians for polar plotting
theta = 2 * np.pi * MLT / 24

# aurora intensity distribution (empirical Gaussian model)
def aurora_intensity(MLAT, theta, peak_mlat=70, width=3, peak_intensity=1):
    """Gaussian intensity distribution centered at peak_mlat."""
    intensity = peak_intensity * np.exp(-((MLAT - peak_mlat)**2) / (2 * width**2))
    return intensity

# magnetic field disturbances (modulation term)
def magnetic_disturbance(MLAT, theta, amp=0.2, freq=3):
    """Simulates magnetic disturbances."""
    return amp * np.sin(freq * theta) * np.exp(-((MLAT - 70)**2) / 10)

# compute auroral intensity (base + disturbance)
intensity = aurora_intensity(MLAT, theta) + magnetic_disturbance(MLAT, theta)

# convert to Cartesian coordinates for geographic visualization
X = MLAT * np.cos(theta)
Y = MLAT * np.sin(theta)

# plotting in apex magnetic latitude/local time (panel b)
fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(8, 8))
c = ax.contourf(theta, MLAT, intensity, levels=50, cmap='plasma')
ax.set_title("Auroral Oval (Apex MLAT/MLT)", fontsize=14)
plt.colorbar(c, label="Photon cm$^{-2}$ s$^{-1}$")

# plotting in geographic coordinates (panel a)
fig, ax = plt.subplots(figsize=(8, 8))
c = ax.contour(X, Y, intensity, levels=50, cmap='plasma')
ax.set_title("Auroral Oval (Geographic Latitude/Longitude)", fontsize=14)
ax.set_xlabel("Geographic X (º)", fontsize=12)
ax.set_ylabel("Geographic Y (º)", fontsize=12)
plt.colorbar(c, label="Photon cm$^{-2}$ s$^{-1}$")
plt.grid()

# geographic projection with coastlines
fig, ax = plt.subplots(figsize=(10, 10), subplot_kw={'projection': ccrs.NorthPolarStereo()})
ax.set_extent([-180, 180, 60, 90], crs=ccrs.PlateCarree())
ax.add_feature(cfeature.COASTLINE, edgecolor='white')

# plot auroral intensity
c = ax.contourf(X, Y, intensity, transform=ccrs.PlateCarree(), cmap='plasma', levels=50)
plt.colorbar(c, label="Photon cm$^{-2}$ s$^{-1}$")
ax.set_title("Auroral Oval with Geographic Context", fontsize=14)

plt.show()
