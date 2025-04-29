import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy
from scipy import *
import os

Dext = 0.42
dz_rs_step = 0.4
Lc = 0.63
dz_s = dz_rs_step * Dext
Rarc = 1.3
zc_arc = Lc + dz_s
theta_low = -20
theta_high = 50
dtheta = .1
epsilon = 0.00003  # Tolerance for matching

# Convert degrees to radians for trigonometric functions
theta_deg = np.arange(theta_low, theta_high + 1, dtheta)
theta_rad = np.radians(theta_deg)

# Arc points
r = Rarc * np.cos(theta_rad)
z = zc_arc + Rarc * np.sin(theta_rad)
frequencies = [500,1500,2500,3500,4500,5500,6500,7500,8500,9500,10500]


def SPL_directivity_input_data(Filename,selectedfrequency, sweep = False):
    if sweep == True:
        # Load the data from the file (skip the metadata lines manually counted; e.g., first 11 lines)
        data = pd.read_csv(Filename, 
                        delim_whitespace=True, 
                        skiprows=11, 
                        header=None, 
                        engine='python')

        frequencies = [500,1500,2500,3500,4500,5500,6500,7500,8500,9500,10500]
        
        columns = ['R', 'Z']

        for freq in frequencies:
            columns += [f' acpr3.Lp_t (dB) @ freq={freq}', f'acpr3.p_t (Pa) @ freq={freq}']

        data.columns = columns

        for freq in frequencies:
            data[f'acpr3.p_t (Pa) @ freq={freq}'] = data[f'acpr3.p_t (Pa) @ freq={freq}'].apply(lambda x: complex(x.replace('i', 'j')))

        return data
    else:
        frequencies = [selectedfrequency]
        # Load the data from the file (skip the metadata lines manually counted; e.g., first 11 lines)
        data = pd.read_csv(Filename, 
                        delim_whitespace=True, 
                        skiprows=11, 
                        header=None, 
                        engine='python')


        
        columns = ['R', 'Z']

        for freq in frequencies:
            columns += [f' acpr3.Lp_t (dB) @ freq={freq}', f'acpr3.p_t (Pa) @ freq={freq}']

        data.columns = columns

        for freq in frequencies:
            data[f'acpr3.p_t (Pa) @ freq={freq}'] = data[f'acpr3.p_t (Pa) @ freq={freq}'].apply(lambda x: complex(x.replace('i', 'j')))

        return data



def SPLplots(selectedfrequency,data,Heightdipole,frequencysweep = False):
    # Step 4: Plot pressure vs arc length
    plt.figure(figsize=(13, 8.5))
    if frequencysweep == True:
        for j in range (len(frequencies)):

            pressure_col = f' acpr3.Lp_t (dB) @ freq={frequencies[j]}'
            pressureoutput = []

            # Prepare data for interpolation
            points = data[['R', 'Z']].values
            values = data[pressure_col].values

            # Interpolate pressure at arc points
            pressureoutput = scipy.interpolate.griddata(points, values, (r, z), method='linear')

            # If some points are still NaN (outside convex hull), fill with nearest
            nan_idx = np.isnan(pressureoutput)
            if np.any(nan_idx):
                pressureoutput[nan_idx] = scipy.interpolate.griddata(points, values, (r[nan_idx], z[nan_idx]), method='nearest')



            # keep only real part of the pressure
            pressureoutput = [p.real for p in pressureoutput]

            # the directivity arc is a curve i want to be able to plot the lenght of this curve vs the sound pressure at those points

            # Step 2: Compute arc lengths
            arc_length = [0]  # Starts at 0
            for i in range(1, len(r)):
                dr = r[i] - r[i - 1]
                dz = z[i] - z[i - 1]
                dL = np.sqrt(dr**2 + dz**2)
                arc_length.append(arc_length[-1] + dL)

            arc_length = np.array(arc_length)


            pressureoutput = pressureoutput[::-1]



            plt.plot(arc_length, pressureoutput, label=f'Frequency: {frequencies[j]} Hz')

        plt.legend(loc='upper right')
        plt.xlabel('Arc Length (m)')
        plt.ylabel('Pressure Magnitude (Pa)')
        plt.title('Pressure Magnitude Along Arc Length')
        plt.grid(True)
        plt.xlim(0, max(arc_length)+0.05)      # Set x-axis limits
        plt.ylim(min(pressureoutput)-5, max(pressureoutput)+5)    # Set y-axis limits
        output_folder = f"OUTPUTS/{Heightdipole}/SPL directivity/"
        os.makedirs(output_folder, exist_ok=True)
        plt.savefig(f"{output_folder}/SPL directivity {Heightdipole} .png", dpi=1000, bbox_inches='tight')
            
            
        plt.close()
        return None




if __name__ == "__main__":
    # Example usage
    # Assuming 'data' is a DataFrame with the required columns
    data = SPL_directivity_input_data("Untitled.txt", 8500, sweep=True)  # Replace with actual data loading
    selectedfrequency = 8500
    Heightdipole = "example_height2"
    frequencysweep = True  # Set to True for frequency sweep
    SPLplots(selectedfrequency,data, Heightdipole, frequencysweep=True)
