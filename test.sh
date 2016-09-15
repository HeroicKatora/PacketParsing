cd $(dirname "$(readlink -f "$0")")
source ./venv/bin/activate
cd src
pip install -e .
python3 -m unittest discover -s ./tests -p "*_test.py"
