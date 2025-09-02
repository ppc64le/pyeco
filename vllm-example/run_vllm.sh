yum install gcc-toolset-13 python3.12-devel python3.12-pip libjpeg-turbo-devel numactl gcc gcc-c++ gcc-gfortran xz cmake yum-utils \
    openssl-devel openblas-devel bzip2-devel bzip2 libffi-devel \
    zlib-devel autoconf automake libtool cargo \
    pkgconf-pkg-config fontconfig fontconfig-devel sqlite-devel -y

source /opt/rh/gcc-toolset-13/enable

python3.12 -m venv venv
source venv/bin/activate

export VLLM_USE_CUSTOM_OPS=0

pip install --no-cache --prefer-binary --extra-index-url https://wheels.developerfirst.ibm.com/ppc64le/linux -r requirements.txt

pip install --no-cache --prefer-binary --extra-index-url https://wheels.developerfirst.ibm.com/ppc64le/linux libprotobuf==4.25.8 openblas

export LD_LIBRARY_PATH=./venv/lib64/python3.12/site-packages/openblas/lib:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=./venv/lib64/python3.12/site-packages/libprotobuf/lib64:$LD_LIBRARY_PATH

python vllm_example.py

echo "====Testing===="
# VLLM needs GPU so just running basic tests
python sub-test1.py
python sub-test2.py
python sub-test3.py
