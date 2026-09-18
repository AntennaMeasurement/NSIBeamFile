
import glob
import os

class AntennaMeasurementNSIBeamFile:
  
  # Constructor initialize class with an folder name containing beam files  
  def __init__(self, folder: str):
    # Check if folder exists
    if not os.path.exists(folder):
        raise ValueError(f"Folder '{folder}' does not exist")
    # Check if folder contians beam files with name pattern "*_beam*.txt"
    beam_files = glob.glob(os.path.join(folder, "*_beam*.txt"))
    if not beam_files:
        raise ValueError(f"No beam files found in folder '{folder}'")
    # Store beam files
    self.beam_files = beam_files
    self.folder = folder
    
    # Parse data from beam files
    self.frequencies = []
    self.skipped_rows = 0
    self.max_rows = 0
    
    for beam_file in self.beam_files:
      with open(beam_file) as file:
        lines = file.readlines()
        for i in range(len(lines)):
          if "Frequency" in lines[i]:
            self.frequencies.append(float(lines[i+2].split()[1]))
            break
    
    with open(beam_files[0]) as file:
      lines = file.readlines()
      for i in range(len(lines)):
        if "P-pol Data" in lines[i]:
          self.skipped_rows = i+1
          break

      for i in range(len(lines)):
        if "X-pol Data" in lines[i]:
          self.max_rows = i+1
          break

    self.max_rows -= self.skipped_rows+2


def hello() -> str:
    return "Hello from AntennaMeasurementNSIBeamFile!"
