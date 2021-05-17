# Hello dear compilerer!

This project is part of my work to write compiler from CPL to QAUD.

# Installation and run the code:
## Installations:
This project write in "python3.x" (x >= 3.6), using the "SLY" library:
```
# Install python3 and pip3
sudo apt install python3
sudo apt install python3-pip

# Install sly
sudo pip3 install sly
```

## Running the compiler:
```
# Go to running location:
cd compilation

# run:
python3 maman_16/cpl_compiler_main.py cpl_code_examples/fibo.ou
# This will produce the file "fibo.par" in the same location as the given file.

# Test: run the qaud file with the qaud interater:
python3 qaud_interpater.py cpl_code_examples/fibo.par
```