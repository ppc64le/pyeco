yum install -y gcc gcc-c++ make
yum install -y python3.12 python3.12-devel python3.12-pip
yum install -y libgfortran


python3.12 -m venv venv
source venv/bin/activate

pip install --no-cache --prefer-binary --extra-index-url https://wheels.developerfirst.ibm.com/ppc64le/linux -r requirements.txt

export LD_LIBRARY_PATH=./venv/lib64/python3.12/site-packages/libprotobuf/lib64:./venv/lib64/python3.12/site-packages/openblas/lib:$LD_LIBRARY_PATH

# echo "USING Granite 3"
# echo "Running: granite3-run.py"
# python granite3-run.py

# echo "Running: test-granite3-classification.py"
# python test-granite3-classification.py

echo "USING Granite 4"
echo "Running: granite4-run.py"
python granite4-run.py

echo "Running: test-granite4-classification.py"
python test-granite4-classification.py
