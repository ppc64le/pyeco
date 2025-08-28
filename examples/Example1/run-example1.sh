sudo dnf install cargo cmake python3.12 python3.12-devel ncurses gcc gcc-c++ libjpeg-devel gfortran --skip-broken --nobest

python3.12 -m venv .venv

source .venv/bin/activate

pip install --prefer-binary --extra-index-url=https://wheels.developerfirst.ibm.com/ppc64le/linux -r requirements.txt 

pip install --upgrade pip

export LD_LIBRARY_PATH=./venv/lib/python3.12/site-packages/openblas/lib:./venv/lib/python3.12/site-packages/libprotobuf/lib64

python3.12 example1.py
python3.12 sub-test1.py
python3.12 sub-test2.py
python3.12 sub-test3.py
