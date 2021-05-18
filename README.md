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
### Linux - Ubuntu
```
# Go to running location:
cd compilation

# Add compilation dir to python path:
export PYTHONPATH=$(pwd)

# run:
python3 maman_16/cpl_compiler_main.py cpl_code_examples/fibo.ou
# This will produce the file "fibo.par" in the same location as the given file.

# Test: run the qaud file with the qaud interater:
python3 qaud_interpater.py cpl_code_examples/fibo.par
```

## Running examples:
![compilation–ADDOP-MLTOP](https://user-images.githubusercontent.com/35425887/118569558-dd380680-b782-11eb-9b27-879210fdc25e.png)
![compilation-and-or](https://user-images.githubusercontent.com/35425887/118569562-df01ca00-b782-11eb-9c8f-9ffdc1bdba2c.png)
![compilation–casting](https://user-images.githubusercontent.com/35425887/118569567-e032f700-b782-11eb-944d-448fd7c70638.png)
![compilation-min](https://user-images.githubusercontent.com/35425887/118569570-e1642400-b782-11eb-93dc-ddea9043f188.png)
![compilation-relop_less_than_equal](https://user-images.githubusercontent.com/35425887/118569571-e1642400-b782-11eb-84e4-66b8fb161c8d.png)
![compilation-while-loop-break-statement-fibonacci-sequence](https://user-images.githubusercontent.com/35425887/118569573-e1fcba80-b782-11eb-846a-bac17956ff15.png)
![compilation-while-loop-fibonacci-sequence](https://user-images.githubusercontent.com/35425887/118569575-e2955100-b782-11eb-800d-8987bcf4b8f6.png)

