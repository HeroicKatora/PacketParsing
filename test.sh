cd $(dirname "$(readlink -f "$0")")
python3 -m unittest discover -s ./src/tests -p "*_test.py"
