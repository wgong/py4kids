## Automation Panda
https://automationpanda.com/2018/10/22/python-testing-101-pytest-bdd/

https://github.com/AndyLPK247/behavior-driven-python/tree/master/pytest-bdd

```
pip install pytest
pip install pytest-bdd
```

### install pipenv


```
$ pip install pipenv

$ git clone https://github.com/AndyLPK247/behavior-driven-python.git

$ cd behavior-driven-python

$ mkdir ~/projects/behavior-driven-python/panda_project
$ cd ~/projects/behavior-driven-python/panda_project
$ python3 -m venv py37

$ . py37/bin/activate

$ virtualenv --python=python3.6 py36


$ pipenv install
$ pipenv shell

pipenv install requests
pipenv install --dev pytest
pipenv run python --version
pipenv run python main.py

```
## Geckodriver
wget https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz
sudo sh -c 'tar -x geckodriver -zf geckodriver-v0.26.0-linux64.tar.gz -O > /usr/local/bin/geckodriver'
sudo chmod +x /usr/local/bin/geckodriver
rm geckodriver-v0.26.0-linux64.tar.gz

## Chromedriver
wget https://chromedriver.storage.googleapis.com/81.0.4044.69/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
sudo chmod +x chromedriver
sudo mv chromedriver /usr/local/bin/
rm chromedriver_linux64.zip
```


### run tests
```
cd ~/projects/behavior-driven-python/pytest-bdd
pip install selenium
pytest tests/step_defs/test_web.py
test_web.py:13: in <module>
    from selenium import webdriver
E   ModuleNotFoundError: No module named 'selenium'
https://medium.com/@shashanksrivastava/how-to-fix-no-module-named-selenium-error-in-python-3-da3fd7b61485

However below works:
python3 -m pytest tests/step_defs/test_web.py

pytest tests/step_defs/test_service.py
pytest tests/step_defs/test_unit_basic.py
pytest tests/step_defs/test_unit_outlines.py
```

### pros/cons
pytest-bdd is best suited for black-box testing because it forces the developer to write test cases in plain, descriptive language. In my opinion, it is arguably the best BDD framework currently available for Python because it rests on the strength and extendability of pytest. However, it can be more cumbersome to use than behave due to the extra code needed for declaring scenarios, implementing scenario outlines, and sharing steps.


### display print stdout/stderr
```
$ behave --no-capture
$ pytest <test_file.py> -s
$ python3 -m pytest tests/step_defs/test_web.py -s
```