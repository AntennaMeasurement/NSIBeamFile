
import glob
import logging
import os
import numpy as np
import matplotlib.pyplot as plt
import time


# Import logging
from NSIBeamFile.log import logger

class NSIBeamFile:
  
  # Constructor initialize class with an folder name containing beam files  
  def __init__(self, folder: str, info: bool = False, debug: bool = False):
    # Check for debug mode and add filter for this class
    self.debug = debug
    self.info = info
    if debug:
      self.info = True
      logger.setLevel(logging.DEBUG)
    if info:
      logger.setLevel(logging.INFO)
      
    class _ClassFilter(logging.Filter):
      def filter(_, record):
        return f"[{self.__class__.__name__}]" in record.getMessage()

    class_filter = _ClassFilter()
    logger.addFilter(class_filter)
    for handler in logger.handlers:
      handler.addFilter(class_filter)
    
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
          
    # sort frequencies in ascending order also match index with beam files
    sorted_indices = np.argsort(self.frequencies)
    self.frequencies = [self.frequencies[i] for i in sorted_indices]
    self.beam_files = [self.beam_files[i] for i in sorted_indices]
    
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
      
      for i in range(len(lines)):
        if "Far-field display setup" in lines[i]:
          self.hangle_size = int(lines[i+2].split()[10])
          self.vangle_size = int(lines[i+5].split()[10])

      self.max_rows -= self.skipped_rows+2
      self.axes = [lines[self.skipped_rows-1].split()[0].replace("(deg)", "").strip(), lines[self.skipped_rows-1].split()[1].replace("(deg)", "").strip()]
      
      if self.debug:
        logger.info(f"[{self.__class__.__name__}] Parsed beam files from folder '{self.folder}': {len(self.beam_files)} files found")
        logger.info(f"[{self.__class__.__name__}] Frequencies: {self.frequencies}")
        logger.info(f"[{self.__class__.__name__}] Skipped rows: {self.skipped_rows}, Max rows: {self.max_rows}")
        logger.info(f"[{self.__class__.__name__}] Axes: {self.axes}")
        logger.info(f"[{self.__class__.__name__}] H-axis size: {self.hangle_size}, V-axis size: {self.vangle_size}")
  
  # Swap axes if needed (e.g., to change the order of hangle and vangle)
  def swap_axes(self) -> None:
          
    # Start chronometer to measure processing time if debug is enabled
    tic = 0.0
    toc = 0.0
    if self.debug:
      tic = time.time()

    for i, beam_file in enumerate(self.beam_files):
      
      hangle, vangle, co_amp, co_phase = np.loadtxt(beam_file, skiprows=self.skipped_rows, max_rows=self.max_rows, unpack=True)
      hangle, vangle, cr_amp, cr_phase = np.loadtxt(beam_file, skiprows=self.skipped_rows+self.max_rows+2, max_rows=self.max_rows, unpack=True)
      
      # Generate angle lists by using min, max and step 
      hangle_list = np.linspace(np.min(hangle), np.max(hangle), self.hangle_size)
      vangle_list = np.linspace(np.min(vangle), np.max(vangle), self.vangle_size)
      
      # Create with empty arrays with zero size for swapped data
      co_amp_swapped = np.ndarray((self.vangle_size, self.hangle_size))
      cr_amp_swapped = np.ndarray((self.vangle_size, self.hangle_size))
      co_phase_swapped = np.ndarray((self.vangle_size, self.hangle_size))
      cr_phase_swapped = np.ndarray((self.vangle_size, self.hangle_size))
        
      vangle_swapped = []
      hangle_swapped = []
      

      for m in range(self.vangle_size):
        mask = (vangle == vangle_list[m])
        # filter amplitude based on the mask
        co_amp_swapped[m, :] = co_amp[mask]
        cr_amp_swapped[m, :] = cr_amp[mask]
        co_phase_swapped[m, :] = co_phase[mask]
        cr_phase_swapped[m, :] = cr_phase[mask]
        for n in range(self.hangle_size):
          vangle_swapped.append(vangle_list[m])
          hangle_swapped.append(hangle_list[n])

      # flattan the swapped arrays
      co_amp_swapped = np.ravel(co_amp_swapped)
      cr_amp_swapped = np.ravel(cr_amp_swapped)
      co_phase_swapped = np.ravel(co_phase_swapped)
      cr_phase_swapped = np.ravel(cr_phase_swapped)

      # Write the swapped data back to the file or a new file
      swapped_data_folder = os.path.join(self.folder, f"{'_'.join(os.path.basename(beam_file).split('_')[:-2])}_Swapped")
      if not os.path.exists(swapped_data_folder):
        os.makedirs(swapped_data_folder)
      
      np.savetxt(os.path.join(swapped_data_folder, f"{self.frequencies[i]:.3f}GHz.csv"), np.column_stack((vangle_swapped, hangle_swapped, co_amp_swapped, co_phase_swapped, cr_amp_swapped, cr_phase_swapped)), header=f"{self.axes[0]}[deg], {self.axes[1]}[deg], CoAmp[dB], CoPhase[deg], CrAmp[dB], CrPhase[deg]", fmt='%.3f, %.3f, %.3f, %.3f, %.3f, %.3f')

    # Stop the chronometer if debug is enabled
    if self.debug:
      toc = time.time()
      logger.debug(f"[{self.__class__.__name__}] Time taken for swapping arrays: {toc - tic:.3f} seconds")
    
  # Export pattern cut data 
  def pattern_cut(self, ax_name: str, ax_value: float, freq: float = 0.0, export: bool = True, plot: bool = False) -> None:
    # Check if frequency is specified and exists in the list of frequencies
    if freq != 0.0 and freq not in self.frequencies:
        raise ValueError(f"Frequency '{freq}' not found in the list of frequencies")
      
    # Check constant axis allow lowercase and uppercase versions
    if ax_name.lower() not in [axis.lower() for axis in self.axes] or ax_name.upper() not in [axis.upper() for axis in self.axes]:
        raise ValueError(f"Invalid axis name'{ax_name}'")
    constant_axis_index = [axis.lower() for axis in self.axes].index(ax_name.lower())
    ax_name = self.axes[constant_axis_index]

    # If frequency is not specified iterate through all beam files
    for i, beam_file in enumerate(self.beam_files):
      # If a specific frequency is specified, skip beam files that do not match the frequency
      if freq != 0.0 and freq != self.frequencies[i]:
        continue
      
      hangle, vangle, co_amp, co_phase = np.loadtxt(beam_file, skiprows=self.skipped_rows, max_rows=self.max_rows, unpack=True)
      hangle, vangle, cr_amp, cr_phase = np.loadtxt(beam_file, skiprows=self.skipped_rows+self.max_rows+2, max_rows=self.max_rows, unpack=True)
      
      axis_angles = [hangle, vangle]
      
      # Checkk if the constant axis value exists in the axis angles
      if ax_value not in axis_angles[constant_axis_index]:
          raise ValueError(f"Constant axis value '{ax_value}' not found in the axis angles")
        
      # Extract the cut data for the specified constant axis value
      sweep_angle  = []
      co_amp_cut   = []
      co_phase_cut = []
      cr_amp_cut   = []
      cr_phase_cut = []
      for j in range(len(axis_angles[constant_axis_index])):
        if axis_angles[constant_axis_index][j] == ax_value:
          sweep_angle.append(axis_angles[1-constant_axis_index][j])
          co_amp_cut.append(co_amp[j])
          co_phase_cut.append(co_phase[j])
          cr_amp_cut.append(cr_amp[j])
          cr_phase_cut.append(cr_phase[j])
      
      if export:
        # Create "Cuts" folder in the same directory as the beam file if it doesn't exist
        cut_data_folder = os.path.join(self.folder, f"{'_'.join(os.path.basename(beam_file).split('_')[:-2])}", "Cut/Data")
        if not os.path.exists(cut_data_folder):
            os.makedirs(cut_data_folder)
        
        # Save the pattern cut data to a file in the "Cuts" folder
        data_file = os.path.join(cut_data_folder, f"{self.frequencies[i]:.3f}GHz_{ax_name}={ax_value:.03f}deg.csv")
        np.savetxt(data_file, np.column_stack((sweep_angle, co_amp_cut, co_phase_cut, cr_amp_cut, cr_phase_cut)), header=f"{self.axes[1-constant_axis_index]}[deg], Co_Amp[dB], Co_Phase[deg], Cross_Amp[dB], Cross_Phase[deg]", fmt='%.3f, %.6f, %.3f, %.6f, %.3f')

      if plot:
        # Create "Cuts" folder in the same directory as the beam file if it doesn't exist
        cut_plot_folder = os.path.join(self.folder, f"{'_'.join(os.path.basename(beam_file).split('_')[:-2])}", "Cut/Plot")
        if not os.path.exists(cut_plot_folder):
            os.makedirs(cut_plot_folder)
            
        plot_file = os.path.join(cut_plot_folder, f"{self.frequencies[i]:.3f}GHz_{ax_name}={ax_value:.03f}deg_amplitude.png")
        plt.figure()
        plt.plot(sweep_angle, co_amp_cut, label="CoPol")
        plt.plot(sweep_angle, cr_amp_cut, label="CrPol")
        plt.xlabel(f"Angle [{self.axes[1-constant_axis_index]}]")
        plt.ylabel("Amplitude [dB]")
        plt.title(f"Pattern Cut at {ax_name}={ax_value:.03f}deg")
        plt.xlim(min(sweep_angle), max(sweep_angle))
        plt.legend()
        plt.grid(True)
        plt.savefig(plot_file)
        plt.close()
        
        plot_file = os.path.join(cut_plot_folder, f"{self.frequencies[i]:.3f}GHz_{ax_name}={ax_value:.03f}deg_phase.png")
        plt.figure()
        plt.plot(sweep_angle, co_phase_cut, label="CoPol")
        plt.plot(sweep_angle, cr_phase_cut, label="CrPol")
        plt.xlabel(f"Angle [{self.axes[1-constant_axis_index]}]")
        plt.ylabel("Phase [deg]")
        plt.title(f"Pattern Cut at {ax_name}={ax_value:.03f}deg")
        plt.xlim(min(sweep_angle), max(sweep_angle))
        plt.ylim((-180.0, 180.0))
        plt.legend()
        plt.grid(True)
        plt.savefig(plot_file)
        plt.close()
    


def hello() -> str:
    return "Hello from NSIBeamFile!"