"""Command line interface for NSIBeamFile."""

from __future__ import annotations

import argparse
import json
import sys

from NSIBeamFile import __version__
from NSIBeamFile.core import NSIBeamFile


def main(argv: list[str] | None = None) -> int:
  argv = sys.argv[1:] if argv is None else argv

  parser = argparse.ArgumentParser(prog="amsnsibeamfile", description="NSIBeamFile Command Line Interface")
  # folfer name as positional argument
  parser.add_argument("folder", help="Measurement data folder that contains the NSI beam files", type=str, nargs=1)
  # flags 
  parser.add_argument("--debug",   action="store_true", help="Enable debug mode")
  parser.add_argument("--info",    action="store_true", help="Enable info mode")
  parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
  # subcommands 
  subparser = parser.add_subparsers(dest="command")
  swap = subparser.add_parser("swap", help="Swap axes in the measurement data and export it")
  export = subparser.add_parser("export", help="Export cut data")
  export.add_argument("--name", help="Constant axis name for the pattern cut", type=str, nargs=1)
  export.add_argument("--value", help="Value for the constant axis in the pattern cut", type=float, nargs=1)
  export.add_argument("--freq", help="Frequency for the pattern cut", type=float, nargs=1)
  plot = subparser.add_parser("plot", help="Plot cut data")
  plot.add_argument("--name", help="Constant axis name for the pattern cut", type=str, nargs=1)
  plot.add_argument("--value", help="Value for the constant axis in the pattern cut", type=float, nargs=1)
  plot.add_argument("--freq", help="Frequency for the pattern cut", type=float, nargs=1)  
  try:
    args = parser.parse_args(argv)
    folder = args.folder[0]
    measurement = NSIBeamFile(folder, debug=args.debug, info=args.info)
    # Construct new parser for subcommands if needed
    if args.command == "swap":
      measurement.swap_axes()
    elif args.command == "export":
      measurement.pattern_cut(constant_axis=args.name[0],
                             constant_axis_value=args.value[0],
                             frequency=args.freq[0],
                             export=True,
                             plot=False)
    elif args.command == "plot":
      measurement.pattern_cut(constant_axis=args.name[0],
                             constant_axis_value=args.value[0],
                             frequency=args.freq[0],
                             export=False,
                             plot=True)
    print(json.dumps({"success": 1}))
    return 0  
  except SystemExit as exc:
    # print(f"SystemExit with code: {exc.code}")
    # argparse's --help/--version actions exit directly; normalize to a return code.
    # print(parser.format_help().replace("positional arguments","module/function"))
    # print(exc.code if isinstance(exc.code, int) else 0)
    if exc.code != 0:
      print(json.dumps({"success": 0, "message": str(exc)}))
    return exc.code if isinstance(exc.code, int) else 0
  # catch all other exceptions
  except Exception as exc:
    print(json.dumps({"success": 0, "message": str(exc)}))
    print(f"{parser.prog}: internal error: {exc}")
    return 1
  




if __name__ == "__main__":
    main()