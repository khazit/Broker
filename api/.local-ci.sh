pytest --cov broker
pylint broker *.py --ignore setup.py && flake8 broker *.py --exclude setup.py 
