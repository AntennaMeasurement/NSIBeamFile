from AntennaMeasurementNSIBeamFile.cli import main


def test_cli_help_no_arguments():
  return_code = main([])
  # Check return code
  assert return_code == 0

def test_cli_help_short():
  return_code = main(["-h"])
  # Check return code
  assert return_code == 0
  
def test_cli_help_long():
  return_code = main(["--help"])
  # Check return code
  assert return_code == 0
  
  
def test_cli_axes():
  return_code = main(["axes", "--folder", "sample_data"])
  # Check return code
  assert return_code == 0
  
def test_cli_frequencies():
  return_code = main(["frequencies", "--folder", "sample_data"])
  # Check return code
  assert return_code == 0

def test_cli_pattern_cut():
  return_code = main(["pattern_cut", "--folder", "sample_data", "--constant_axis", "theta", "--constant_axis_value", "90.0", "--frequency", "10.0", "--export", "--plot"])
  # Check return code
  assert return_code == 0