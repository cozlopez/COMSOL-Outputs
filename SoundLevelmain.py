from src.SPL_directivity_arc import SPL_directivity_input_data
from src.SoundPressureLevel import Soundlevelplots
import sys
import os
availablefrequencies = [500,1500,2500,3500,4500,5500,6500,7500,8500,9500,10500]
foldercounter = os.path.join(os.path.dirname(__file__), 'DATA/')
selectedfrequency = 8500
for y in range(len(next(os.walk(foldercounter))[1])):
    
    shortpath = f'DATA/zd_{y+1}/fullset/Untitled.txt'
    Heightdipole = f'zd_{y+1}'


    # Check if the file exists
    if not os.path.exists(shortpath):
        continue  # Skip this iteration if file does not exist
    



    data = SPL_directivity_input_data(shortpath,8500, sweep = True) # No sweep
    Soundlevelplots(data, 8500, Heightdipole , frequencysweep = True) # No sweep
