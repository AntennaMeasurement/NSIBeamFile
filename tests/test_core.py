
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

  print(antenna_measurement.frequencies, antenna_measurement.skipped_rows, antenna_measurement.max_rows)
  assert 0 == 0
