# AntennaMeasurement NSIBeamFile Python Package and CLI

This package provides tools for working with NSI beam files.

## Features
- Access far-field axes declared in NSI beam files
- Access frequencies declared in NSI beam files
- Export pattern cut data from NSI beam files
- Plot pattern cut data from NSI beam files

## Installation

You can install the package using `pip`:

```bash
pip install NSIBeamFile
```

## CLI

The command line interface allows you to interact with the AntennaMeasurement NSIBeamFile package directly from the terminal. You can use the following commands:

- `axes`: Access far-field axes declared in NSI beam files
- `frequencies`: Access frequencies declared in NSI beam files
- `pattern_cut`: Export and plot pattern cut data from NSI beam files

Use the `--help` flag with any command to see the available options.

## Standalone executable

The CLI can be bundled into a single executable with PyInstaller. Build on the
same operating system and architecture where the executable will be used.

### Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[build]"
python -m PyInstaller --clean NSIBeamFile.spec
```

The executable is created at
`dist\NSIBeamFileCli.exe`.

### Linux or macOS

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e '.[build]'
python -m PyInstaller --clean NSIBeamFile.spec
```

The executable is created at `dist/NSIBeamFileCli`.

Run the executable from a directory containing the measurement data, or pass
an explicit data-folder path:

```text
NSIBeamFileCli axes --folder sample_data
NSIBeamFileCli frequencies --folder sample_data
NSIBeamFileCli pattern_cut --folder sample_data --constant_axis theta --constant_axis_value 90 --frequency 10 --export
```
