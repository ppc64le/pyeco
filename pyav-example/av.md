PyAV Installation Test
This project has easy tests to check if PyAV and some other packages (ml_dtypes, llvmlite, Pillow) are installed and working.

How to Run
Put the files example.py, subtest.py, and run_av.sh in one folder.

Open a terminal and run:
./run_av.sh

This script will install what you need and run the tests.

What It Tests
PyAV can be used to make videos.
Pillow can create images.
ml_dtypes works with special number types.
llvmlite can run simple code.

All these packages work together.

If you get errors about codecs (like mpeg4), it means your FFmpeg doesn’t support them. The tests will use other codecs.
Make sure FFmpeg is installed and available on your system.
Running these tests helps you check that everything is set up correctly.
