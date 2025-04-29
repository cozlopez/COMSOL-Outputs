from src.SPL_directivity_arc import SPL_directivity_input_data, SPLplots

shortpath = "Untitled.txt"
Heightdipole = '0.4'
selectedfre


data = SPL_directivity_input_data(shortpath,selectedfrequency) # No sweep
# data = SPL_directivity_input_data("Untitled2.txt",sweep=True) # Sweep (selectedfrequency in this case is not used but still give a random value)
SPLplots(selectedfrequency,data,Heightdipole) # No sweep