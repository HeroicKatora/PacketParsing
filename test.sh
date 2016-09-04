cd $(dirname "$(readlink -f "$0")")
source ./venv/bin/activate
python3 -m unittest discover -s ./src/tests -p "*_test.py"
