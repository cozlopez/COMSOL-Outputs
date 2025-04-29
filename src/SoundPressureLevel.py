import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as tri
import os


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


def Soundlevelplots(data, selectedfrequency, Heightdipole, frequencysweep = False):
    # Extract the relevant columns from the data

    
    if frequencysweep == True:
        frequencies = [500,1500,2500,3500,4500,5500,6500,7500,8500,9500,10500]

        for j in range (len(frequencies)):
        
            # Extract cylindrical coordinates and convert to Cartesian
            pressure_col = f' acpr3.Lp_t (dB) @ freq={frequencies[j]}'
            pressureoutput = []
            mask_circle = (data['R']**2 + (data['Z'] - 0.8)**2) <= 16

            # Mask for the vertical line from (4, 0.8) down to (4, 0)
            mask_line = (data['R'] >= 0) & (data['R'] <= 4) & (data['Z'] <= 0.8) & (data['Z'] >= 0)

            # Combine both masks
            mask = mask_circle | mask_line
            data = data[mask]
            R = data['R'].values
            Z = data['Z'].values
            

            P_complex = data[pressure_col].values

            P_real = P_complex.real  # Physical sound pressure oscillation

            # Create a triangulation for contour plotting
            triang = tri.Triangulation(R, Z)

            # Define symmetric color scale limits
            vmin, vmax = 40,65

            # Create levels for a **linear** color distribution
            levels = np.linspace(vmin, vmax, 500)
            

            # Plot the field
            plt.figure(figsize=(8, 6))
            contour = plt.tricontourf(triang, P_real, cmap='jet', levels=levels, extend='both')
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
            output_folder = f"OUTPUTS/{Heightdipole}/{frequencies[j]}"
            os.makedirs(output_folder, exist_ok=True)
            plt.savefig(f"{output_folder}/Sound_Level_{frequencies[j]}_Hz_{Heightdipole}.png", dpi=1000, bbox_inches='tight')
    else:
            frequencies = [selectedfrequency]
        # Extract cylindrical coordinates and convert to Cartesian
            pressure_col = f' acpr3.Lp_t (dB) @ freq={frequencies[0]}'
            pressureoutput = []
            mask_circle = (data['R']**2 + (data['Z'] - 0.8)**2) <= 16

            # Mask for the vertical line from (4, 0.8) down to (4, 0)
            mask_line = (data['R'] >= 0) & (data['R'] <= 4) & (data['Z'] <= 0.8) & (data['Z'] >= 0)

            # Combine both masks
            mask = mask_circle | mask_line
            data = data[mask]
            R = data['R'].values
            Z = data['Z'].values
            

            P_complex = data[pressure_col].values

            P_real = P_complex.real  # Physical sound pressure oscillation

            # Create a triangulation for contour plotting
            triang = tri.Triangulation(R, Z)

            # Define symmetric color scale limits
            vmin, vmax = 40,65

            # Create levels for a **linear** color distribution
            levels = np.linspace(vmin, vmax, 500)
            

            # Plot the field
            plt.figure(figsize=(8, 6))
            contour = plt.tricontourf(triang, P_real, cmap='jet', levels=levels, extend='both')
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
            output_folder = f"OUTPUTS/{Heightdipole}/{frequencies}"
            os.makedirs(output_folder, exist_ok=True)
            plt.savefig(f"{output_folder}/Sound_Level_{frequencies}_Hz_{Heightdipole}.png", dpi=1000, bbox_inches='tight')