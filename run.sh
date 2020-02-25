DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"
cd "venv"
cd "Scripts"
source activate

cd "$DIR"

python app.py

read -n1 -r -p "Press any key to continue..." key