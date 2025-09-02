yum install gcc-toolset-13 python3.11-devel python3.11-pip -y
source /opt/rh/gcc-toolset-13/enable

python3.11 -m venv venv
source venv/bin/activate

pip install --no-cache --prefer-binary --extra-index-url https://wheels.developerfirst.ibm.com/ppc64le/linux -r requirements.txt

pip install libprotobuf==4.25.8 openblas --no-cache --prefer-binary --extra-index-url https://wheels.developerfirst.ibm.com/ppc64le/linux

export LD_LIBRARY_PATH=./venv/lib64/python3.11/site-packages/libprotobuf/lib64:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=./venv/lib64/python3.11/site-packages/openblas/lib:$LD_LIBRARY_PATH

python pytorch_example.py

echo "==== Running tests ===="

python sub-test1.py
python sub-test2.py
python sub-test3.py
