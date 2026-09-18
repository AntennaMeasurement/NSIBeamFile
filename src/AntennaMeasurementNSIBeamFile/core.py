
import glob
import os
import numpy as np

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
    self.frequencies  = []
    self.axes         = []
    self.skipped_rows = 0
    self.max_rows     = 0
    
    for beam_file in self.beam_files:
      with open(beam_file) as file:
        lines = file.readlines()
        for i in range(len(lines)):
          if "Frequency" in lines[i]:
            self.frequencies.append(float(lines[i+2].split()[1]))
            break
    
    with open(self.beam_files[0]) as file:
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
      self.axes = [lines[self.skipped_rows-1].split()[0].replace("(deg)", "").strip(), lines[self.skipped_rows-1].split()[1].replace("(deg)", "").strip()]
    
    
  # Export pattern cut data 
  def export_pattern_cut(self, constant_axis: str, constant_axis_value: float, frequency: float = 0.0) -> None:
    # Check if frequency is specified and exists in the list of frequencies
    if frequency != 0.0 and frequency not in self.frequencies:
        raise ValueError(f"Frequency '{frequency}' not found in the list of frequencies")
      
    # Check constant axis allow lowercase and uppercase versions
    if constant_axis.lower() not in [axis.lower() for axis in self.axes] or constant_axis.upper() not in [axis.upper() for axis in self.axes]:
        raise ValueError(f"Invalid constant_axis '{constant_axis}'")
    constant_axis_index = [axis.lower() for axis in self.axes].index(constant_axis.lower())

    # If frequency is not specified iterate through all beam files
    for i, beam_file in enumerate(self.beam_files):
      hangle, vangle, co_amp, co_phase = np.loadtxt(beam_file, skiprows=self.skipped_rows, max_rows=self.max_rows, unpack=True)
      hangle, vangle, cr_amp, cr_phase = np.loadtxt(beam_file, skiprows=self.skipped_rows+self.max_rows+2, max_rows=self.max_rows, unpack=True)
      
      axis_angles = [hangle, vangle]
      
      # Checkf if the constant axis value exists in the axis angles
      if constant_axis_value not in axis_angles[constant_axis_index]:
          raise ValueError(f"Constant axis value '{constant_axis_value}' not found in the axis angles")
        
      # Extract the cut data for the specified constant axis value
      sweep_angle  = []
      co_amp_cut   = []
      co_phase_cut = []
      cr_amp_cut   = []
      cr_phase_cut = []
      for j in range(len(axis_angles[constant_axis_index])):
        if axis_angles[constant_axis_index][j] == constant_axis_value:
          sweep_angle.append(axis_angles[1-constant_axis_index][j])
          co_amp_cut.append(co_amp[j])
          co_phase_cut.append(co_phase[j])
          cr_amp_cut.append(cr_amp[j])
          cr_phase_cut.append(cr_phase[j])
      
 
      # Create "Cuts" folder in the same directory as the beam file if it doesn't exist
      cuts_folder = os.path.join(os.path.dirname(beam_file), "Cut/Data")
      if not os.path.exists(cuts_folder):
          os.makedirs(cuts_folder)
          
      # Save the pattern cut data to a file in the "Cuts" folder
      cut_file = os.path.join(cuts_folder, f"{self.frequencies[i]:.3f}GHz_{constant_axis}={constant_axis_value:.03f}deg.csv")
      np.savetxt(cut_file, np.column_stack((sweep_angle, co_amp_cut, co_phase_cut, cr_amp_cut, cr_phase_cut)), header="Angle[deg], Co_Amp[dB], Co_Phase[deg], Cross_Amp[dB], Cross_Phase[deg]", fmt='%.3f, %.6f, %.3f, %.6f, %.3f')



def hello() -> str:
    return "Hello from AntennaMeasurementNSIBeamFile!"