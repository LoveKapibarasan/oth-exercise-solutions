
sudo zypper install python3 python3-pip python3-setuptools python3-wheel
python3 -m venv .venv && source .venv/bin/activate 
pip install -r requirements.txt

jupyter lab