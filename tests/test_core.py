
def test_hello():
  from NSIBeamFile.core import hello
  expected = "Hello from NSIBeamFile!"
  captured = hello()
  assert captured == expected
  
def test_antenna_measurement_nsi_beam_file_init():
  from NSIBeamFile.core import NSIBeamFile

  sample_folder = "sample_data" 

  # Initialize the class
  antenna_measurement = NSIBeamFile(sample_folder)

  print(antenna_measurement.frequencies, antenna_measurement.skipped_rows, antenna_measurement.max_rows, antenna_measurement.axes)
  assert 0 == 0
  
def test_swap_axes():
  from NSIBeamFile.core import NSIBeamFile

  sample_folder = "sample_data" 

  # Initialize the class
  antenna_measurement = NSIBeamFile(sample_folder)

  # Swap axes for testing
  antenna_measurement.swap_axes()

  assert 0 == 0

def test_export_pattern_cut():
  from NSIBeamFile.core import NSIBeamFile

  sample_folder = "sample_data" 

  # Initialize the class
  antenna_measurement = NSIBeamFile(sample_folder)

  # Export a pattern cut for testing
  constant_axis = "theta"
  constant_axis_value = 90.0
  # constant_axis = "phi"
  # constant_axis_value = 0.0
  frequency = antenna_measurement.frequencies[0]
  antenna_measurement.pattern_cut(constant_axis, constant_axis_value, frequency, export=True, plot=True)

  assert 0 == 0

