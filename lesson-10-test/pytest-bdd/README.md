## Automation Panda
https://automationpanda.com/2018/10/22/python-testing-101-pytest-bdd/

https://github.com/AndyLPK247/behavior-driven-python/tree/master/pytest-bdd


### install pipenv

$ pip install pipenv

$ git clone https://github.com/AndyLPK247/behavior-driven-python.git

$ cd behavior-driven-python

$ pipenv install
$ pipenv shell

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
pytest tests/step_defs/test_web.py
pytest tests/step_defs/test_service.py
pytest tests/step_defs/test_unit_basic.py
pytest tests/step_defs/test_unit_outlines.py


pros/cons
pytest-bdd is best suited for black-box testing because it forces the developer to write test cases in plain, descriptive language. In my opinion, it is arguably the best BDD framework currently available for Python because it rests on the strength and extendability of pytest.
However, it can be more cumbersome to use than behave due to the extra code needed for declaring scenarios, implementing scenario outlines, and sharing steps.
