export SUPERNADO_PATH=$(pwd)
export SUPERNADO_SERVICE=$1
export PATH="~/miniconda/bin:$PATH"
source activate $1
python services/$1/main.py
