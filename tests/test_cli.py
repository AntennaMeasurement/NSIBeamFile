from NSIBeamFile.cli import main


def test_cli_help_short():
  return_code = main(["-h"])
  # Check return code
  assert return_code == 0
  
def test_cli_help_long():
  return_code = main(["--help"])
  # Check return code
  assert return_code == 0

def test_cli_version():
  return_code = main(["--version"])
  # Check return code
  assert return_code == 0

def test_cli_help_no_arguments():
  return_code = main([])
  # Should return 2 since no arguments are provided
  assert return_code == 2

def test_cli_invalid_folder_argument():
  # Return exception code
  return_code = main(["non_existent_folder"])
  assert return_code != 0
 
def test_cli_valid_folder_argument():
  # Return exception code
  return_code = main(["sample_data"])
  assert return_code == 0
  
def test_cli_swap_command_help():
  return_code = main(["sample_data", "swap", "-h"])
  assert return_code == 0

def test_cli_swap_command():
  return_code = main(["sample_data", "--debug", "swap"])
  assert return_code == 0
  
def test_cli_export_command_help():
  return_code = main(["sample_data", "export", "-h"])
  assert return_code == 0

def test_cli_export_command():
  return_code = main(["sample_data", "--info", "export", "--name", "theta", "--value", "90.0", "--freq", "10.0"])
  assert return_code == 0
  
def test_cli_plot_command_help():
  return_code = main(["sample_data", "plot", "-h"])
  assert return_code == 0
  
def test_cli_plot_command():
  return_code = main(["sample_data", "--info", "plot", "--name", "theta", "--value", "90.0", "--freq", "10.0"])
  assert return_code == 0
  
