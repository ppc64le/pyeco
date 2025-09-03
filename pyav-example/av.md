# PyAV Installation Test
This project provides a simple and robust test to verify the successful installation and functionality of the PyAV package and its underlying FFmpeg dependencies.

## How to Run
1. Place the `av-example.py` and `av.sh` scripts in the same directory.
2. Run the main shell script from your terminal:

./run_av.sh
The `run_av.sh` script will automatically handle the installation of system dependencies, create a virtual environment, install the necessary Python packages, and run the tests to confirm that your setup is working.

## What It Tests
The `av-example.py` script performs two key checks:
- PyAV Import: It verifies that the `av` package and its linked FFmpeg libraries can be successfully imported and accessed from Python.
- FFmpeg Binary: It checks for the presence and functionality of the `ffmpeg` command-line tool, which is a required dependency.
If the script runs without errors, your PyAV installation is correctly configured.
