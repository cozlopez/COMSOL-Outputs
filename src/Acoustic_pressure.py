import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as tri

# Load data (Ensure "i" is replaced with "j" for complex numbers)
filename = "Untitled2.txt"
with open(filename, "r") as f:
    lines = [line.replace("i", "j") for line in f]



lines = [line for line in lines if not line.strip().startswith('%')]
data = np.loadtxt(lines, dtype=complex)

# Load nozzle area data no complex just r and z
filename = "contractionProfile.txt"
with open(filename , "r") as f:
    lines = f.readlines()

nozzle_area = np.loadtxt(lines)
# Turn data by line of symmetry y=z to turn upright
#nozzle_area = np.vstack((nozzle_area, nozzle_area[:,::-1]))

# Flip the axis of the nozzle area to match the data
nozzle_area = nozzle_area[:,::-1]
#make symetry around z=0
nozzle_area = np.vstack((nozzle_area, nozzle_area[:,::-1]))
rotated_nozzle_area = np.zeros_like(nozzle_area)
rotated_nozzle_area[:,0] = nozzle_area[:,1]
rotated_nozzle_area[:,1] = nozzle_area[:,0]
nozzle_area = rotated_nozzle_area
# create a circle size 4.5 to plot for positive quadrant 
# create a circle size 4.5 centered around (0, 1) to plot for positive quadrant
circle = np.zeros((100, 2))
circle[:, 0] = 4 * np.cos(np.linspace(0, np.pi / 2, 100))
circle[:, 1] = 4 * np.sin(np.linspace(0, np.pi / 2, 100)) +0.8





# Extract cylindrical coordinates and convert to Cartesian
R = data[:, 0].real  # Radial coordinate
Z = data[:, 1].real  # Axial coordinate
P_complex = data[:, 3]  # Complex sound pressure

# Convert to Cartesian (Y-Z plane)
Y = R
X = np.zeros_like(Y)  # Since it's a 2D slice

# Use the real part of the sound pressure
P_real = P_complex.real  # Physical sound pressure oscillation

# Create a triangulation for contour plotting
triang = tri.Triangulation(Y, Z)

# Define symmetric color scale limits
vmin, vmax = -0.04, 0.04

# Create levels for a **linear** color distribution
levels = np.linspace(vmin, vmax, 500)

# Plot the field
plt.figure(figsize=(8, 6))
contour = plt.tricontourf(triang, P_real, cmap='seismic', levels=levels, extend='both')
cbar = plt.colorbar(contour, ticks=np.linspace(vmin, vmax, 5))
cbar.set_label("Real Part of Sound Pressure (Pa)")
# Plot black line connecting all points in nozzle area
plt.plot(nozzle_area[:,0], nozzle_area[:,1]*1.2912, color='black',linewidth=1)
# plot quadrant
plt.plot(circle[:,0], circle[:,1], color='black',linewidth=1.5)
plt.plot([4, 4], [0.8, 0], color='black',linewidth=1.5)
plt.plot([0.21, 0.2771134021],[0.48* 1.2912, 0.48* 1.2912], color='black',linewidth=1.5)
plt.plot([0, 0],[4.8, 0.48* 1.2912+0.005], color='black',linewidth=1.5)
plt.plot([0.3,4],[0,0], color='black',linewidth=1.5)

# Set aspect ratio to 1:1
plt.axis('equal')
# Black out the area between the contraction profile and the x = 0 wall
x_blackout = np.concatenate((nozzle_area[:, 0], [0, 0]))  # Add x = 0 for the left wall
y_blackout = np.concatenate((nozzle_area[:, 1] * 1.2912, [nozzle_area[:, 1].max() * 1.2912, nozzle_area[:, 1].min() * 1.2912]))  # Add corresponding y values
plt.fill(x_blackout, y_blackout, color='white', zorder=1)

# Labels and display
plt.xlabel("Y (m)")
plt.ylabel("Z (m)")
plt.title("Acoustic Pressure Distribution in Y-Z Plane")
plt.grid(True)
plt.show()
