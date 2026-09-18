
def test_hello():
  from AntennaMeasurementNSIBeamFile.core import hello
  expected = "Hello from AntennaMeasurementNSIBeamFile!"
  captured = hello()
  assert captured == expected
  
def test_antenna_measurement_nsi_beam_file_init():
  from AntennaMeasurementNSIBeamFile.core import AntennaMeasurementNSIBeamFile

  sample_folder = "sample_data" 

  # Initialize the class
  antenna_measurement = AntennaMeasurementNSIBeamFile(sample_folder)

  print(antenna_measurement.frequencies, antenna_measurement.skipped_rows, antenna_measurement.max_rows, antenna_measurement.axes)
  assert 0 == 0

def test_export_pattern_cut():
  from AntennaMeasurementNSIBeamFile.core import AntennaMeasurementNSIBeamFile

  sample_folder = "sample_data" 

  # Initialize the class
  antenna_measurement = AntennaMeasurementNSIBeamFile(sample_folder)

  # Export a pattern cut for testing
  constant_axis = "theta"
  constant_axis_value = 0.0
  frequency = antenna_measurement.frequencies[0]
  antenna_measurement.export_pattern_cut(constant_axis, constant_axis_value, frequency)

  assert 0 == 0
  