# Drive/Folder Size Scanner

A simple Python/Tkinter application to scan a drive or folder and display the size of each subfolder in a sortable tree view.

## Features

- **Recursive scanning:** Traverses all subdirectories under a selected root.
- **Size aggregation:** Calculates individual file sizes and rolls them up into parent folders.
- **Human-readable output:** Formats sizes in B, KB, MB, GB, etc.
- **Sortable view:** Sort by ascending or descending folder size.
- **Responsive UI:** Scanning runs in a background thread to keep the GUI responsive.
- **Cross-platform:** Works on Windows, macOS, and Linux (with Python and Tkinter installed).

## Requirements

- Python 3.6+
- Tkinter (usually bundled with standard Python)
- `pip` (for any future dependencies)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/file-scanner.git
   cd file-scanner
