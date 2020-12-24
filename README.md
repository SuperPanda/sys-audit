hhttp://medium.com/@jtpaasch/the-right-way-to-use-virtual-environments-1bc255a0cba7
python -m pip --versopm
python -m pip install --upgrade pip
pip install virtualenv
virtualenv env
source env/bin/activate
pip install -r requirement.txt
p
# To save new requirements.txt
pip freeze > requirement.txt
