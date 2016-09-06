export PATH="~/miniconda/bin:$PATH"
source activate $1
python services/$1/main.py
