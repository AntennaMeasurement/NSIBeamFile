# NSIBeamFile

NSIBeamFile parses NSI2000 far-field beam files and provides Python and command-line tools for swapping axes and exporting or plotting pattern cuts.

## Features

- Read the far-field axes and frequencies declared in NSI beam files.
- Swap the beam-file axes and export the result as CSV files.
- Export co-polarized and cross-polarized pattern-cut data as CSV files.
- Plot pattern-cut amplitude and phase data as PNG files.

## Installation

Install the package from PyPI:

```bash
python -m pip install NSIBeamFile
```

For a local development installation, including the test dependencies:

```bash
python -m pip install -e ".[test]"
```

## Command-line usage

The CLI expects a folder containing files matching `*_beam*.txt`:

```bash
amnsibeamfile FOLDER COMMAND [OPTIONS]
```

Available commands:

- `swap`: Swap the beam-file axes and export CSV files.
- `export`: Export pattern-cut data.
- `plot`: Plot pattern-cut amplitude and phase data.

Examples:

```bash
amnsibeamfile sample_data swap
amnsibeamfile sample_data export --ax_name theta --ax_value 90.0
amnsibeamfile sample_data export --ax_name theta --ax_value 90.0 --freq 10.0
amnsibeamfile sample_data plot --ax_name theta --ax_value 90.0 --freq 10.0
```

Use `amnsibeamfile --help` or `amnsibeamfile FOLDER COMMAND --help` for the
complete option list. Add `--info` or `--debug` before the command to enable
logging.

## Python usage

```python
from NSIBeamFile.core import NSIBeamFile

measurement = NSIBeamFile("sample_data")
print(measurement.axes)
print(measurement.frequencies)

measurement.pattern_cut(
    ax_name="theta",
    ax_value=90.0,
    freq=10.0,
    export=True,
    plot=True,
)
```

Pattern-cut data is written below the measurement folder in `Cut/Data`, and
plots are written in `Cut/Plot`. Swapped data is written to a sibling folder
whose name ends in `_Swapped`.

## Building a standalone executable

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

The executable is created at `dist\amnsibeamfile.exe`.

### Linux or macOS

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e '.[build]'
python -m PyInstaller --clean NSIBeamFile.spec
```

The executable is created at `dist/amnsibeamfile`.

Run the executable from a directory containing the measurement data, or pass
an explicit data-folder path:

```text
amnsibeamfile sample_data swap
amnsibeamfile sample_data export --ax_name theta --ax_value 90.0 --freq 10.0
```
