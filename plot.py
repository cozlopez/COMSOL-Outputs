import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as tri

# Load data (Ensure "i" is replaced with "j" for complex numbers)
filename = "Untitled.txt"
with open(filename, "r") as f:
    lines = [line.replace("i", "j") for line in f]

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
circle = np.zeros((100,2))
circle[:,0] = 4.7*np.cos(np.linspace(0, np.pi/2, 100))
circle[:,1] = 4.7*np.sin(np.linspace(0, np.pi/2, 100))





# Extract cylindrical coordinates and convert to Cartesian
R = data[:, 0].real  # Radial coordinate
Z = data[:, 1].real  # Axial coordinate
P_complex = data[:, 2]  # Complex sound pressure

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
plt.plot(nozzle_area[:,0], nozzle_area[:,1], color='black')
# plot quadrant
plt.plot(circle[:,0], circle[:,1])
# Set aspect ratio to 1:1
plt.axis('equal')

# Labels and display
plt.xlabel("Y (m)")
plt.ylabel("Z (m)")
plt.title("Acoustic Pressure Distribution in Y-Z Plane")
plt.grid(True)
plt.show()
