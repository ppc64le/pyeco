sudo dnf install -y python3.12 python3.12-devel python3.12-pip gcc-toolset-13 libjpeg-turbo-devel

source /opt/rh/gcc-toolset-13/enable

python3.12 -m venv .venv

source .venv/bin/activate

pip install --prefer-binary --extra-index-url=https://wheels.developerfirst.ibm.com/ppc64le/linux -r requirements.txt

pip install --upgrade pip

export LD_LIBRARY_PATH=./.venv/lib/python3.12/site-packages/openblas/lib:$LD_LIBRARY_PATH

echo -e "\nRunning example2.py"
python3.12 example2.py

echo -e "\nRunning sub-test1.py"
python3.12 sub-test1.py

echo -e "\nRunning sub-test2.py"
python3.12 sub-test2.py

echo -e "\nRunning sub-test3.py"
python3.12 sub-test3.py

echo -e "\nRunning sub-test4.py"
python3.12 sub-test4.py

echo -e "\nRunning sub-test5.py"
python3.12 sub-test5.py
