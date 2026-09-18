"""Command line interface for AntennaMeasurementNSIBeamFile."""

from __future__ import annotations

import argparse
import json
import sys

from AntennaMeasurementNSIBeamFile import __version__
from AntennaMeasurementNSIBeamFile.core import AntennaMeasurementNSIBeamFile


def main(argv: list[str] | None = None) -> int:
  argv = sys.argv[1:] if argv is None else argv

  if argv and argv[0] == "axes":
    parser = argparse.ArgumentParser(prog="axes", description="Far-field axes declared in NSI beam files")
    parser.add_argument("--folder", help="Measurement data folder that contains the NSI beam files", type=str, nargs=1)
    try:
      args = parser.parse_args(argv[1:])
    except SystemExit as exc:
      # argparse's --help/--version actions exit directly; normalize to a return code.
      return exc.code if isinstance(exc.code, int) else 0
    if args.folder:
      folder = args.folder[0]
      measurement = AntennaMeasurementNSIBeamFile(folder)
      print(json.dumps({"success": 1, "axes": measurement.axes}))
      return 0
    else:
      print(json.dumps({"success": 0, "error": "Folder argument is required"}))
      return 1
    
  
  elif argv and argv[0] == "frequencies":
    parser = argparse.ArgumentParser(prog="frequencies", description="Frequencies declared in NSI beam files")
    parser.add_argument("--folder", help="Measurement data folder that contains the NSI beam files", type=str, nargs=1)
    try:
      args = parser.parse_args(argv[1:])
    except SystemExit as exc:
      # argparse's --help/--version actions exit directly; normalize to a return code.
      return exc.code if isinstance(exc.code, int) else 0
    if args.folder:
      folder = args.folder[0]
      measurement = AntennaMeasurementNSIBeamFile(folder)
      print(json.dumps({"success": 1, "frequencies": measurement.frequencies}))
      return 0
    else:
      print(json.dumps({"success": 0, "error": "Folder argument is required"}))
      return 1
  
  elif argv and argv[0] == "pattern_cut":
    parser = argparse.ArgumentParser(prog="pattern_cut", description="Export pattern cut data from NSI beam files")
    parser.add_argument("--folder", help="Measurement data folder that contains the NSI beam files", type=str, nargs=1)
    parser.add_argument("--constant_axis", help="Constant axis name for the pattern cut like theta, phi ...", type=str, nargs=1)
    parser.add_argument("--constant_axis_value", help="Value of the constant axis for the pattern cut in degrees", type=float, nargs=1)
    parser.add_argument("--frequency", help="Frequency in the pattern cut data you are interested in GHz", type=float, nargs="?")
    parser.add_argument("--export", help="Export the pattern cut data default behavior is True (can be disabled with --no-export)", action="store_true")
    parser.add_argument("--plot", help="Plot the pattern cut data", action="store_true")
    try:
      args = parser.parse_args(argv[1:])
    except SystemExit as exc:
      return exc.code if isinstance(exc.code, int) else 0
    if args.folder and args.constant_axis and args.constant_axis_value:
      folder = args.folder[0]
      constant_axis = args.constant_axis[0]
      constant_axis_value = args.constant_axis_value[0]
      frequency = args.frequency if args.frequency else 0.0
      export = args.export if args.export else True
      plot = args.plot
      measurement = AntennaMeasurementNSIBeamFile(folder)
      measurement.pattern_cut(constant_axis, constant_axis_value, frequency, export, plot)
      return 0
    else:
      print(json.dumps({"success": 0, "error": "Folder, constant_axis, and constant_axis_value arguments are required"}))
      return 1
  
  
  else:
    parser = argparse.ArgumentParser(prog="AntennaMeasurementNSIBeamFileCli", description="NSIBeamFile Command Line Interface")
    parser.add_argument("axes", help="Far-field axes declared in NSI beam files", type=str, nargs="?")
    parser.add_argument("frequencies", help="Frequencies declared in NSI beam files", type=str, nargs="?")
    parser.add_argument("pattern_cut", help="Export and plot pattern cut data from NSI beam files", type=str, nargs="?")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    try:
      args = parser.parse_args(argv)
    except SystemExit as exc:
      # argparse's --help/--version actions exit directly; normalize to a return code.
      return exc.code if isinstance(exc.code, int) else 0
    print(parser.format_help().replace("positional arguments","module/function"))
    return 0



if __name__ == "__main__":
    main()