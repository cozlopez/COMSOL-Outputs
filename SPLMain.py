from src.SPL_directivity_arc import *
import sys
import os
from pathlib import Path
from src.filepath_extraction import get_single_subpath_part as gp

foldercounter = os.path.join(os.path.dirname(__file__), 'DATA/')
availablefrequencies = [500,1500,2500,3500,4500,5500,6500,7500,8500,9500,10500]
for y in range(len(next(os.walk(foldercounter))[1])):
    for h in range(len(availablefrequencies)):
        shortpath = f'DATA/zd_{y+1}/{availablefrequencies[h]}/Untitled.txt'
        Heightdipole = f'zd_{y+1}'
        parentpath = f'{availablefrequencies[h]}'
 
        # Check if the file exists
        if not os.path.exists(shortpath):
            continue  # Skip this iteration if file does not exist
    
        for freq in availablefrequencies:
            if freq == int(parentpath):
                selectedfrequency = freq
            else:
                continue


        data = SPL_directivity_input_data(shortpath,selectedfrequency) # No sweep
        # data = SPL_directivity_input_data("Untitled2.txt",sweep=True) # Sweep (selectedfrequency in this case is not used but still give a random value)
        SPLplots(selectedfrequency,data,Heightdipole) # No sweep
        # SPLplots(8500,data,Heightdipole=0.8,frequencysweep=True) # Sweep (selectedfrequency in this case is not used but still give a random value)
