# [FlaskAPI](https://www.flaskapi.org/)

`pip install Flask-API`


## Example 1 - Notes

### start flask server at http://127.0.0.1:5000/
`$ python flask_notes.py`

### curl to test

`get all keys`
$ curl -X GET http://127.0.0.1:5000/
[{"url": "http://127.0.0.1:5000/0/", "text": "do the shopping"}, {"url": "http://127.0.0.1:5000/1/", "text": "build the codez"}, {"url": "http://127.0.0.1:5000/2/", "text": "paint the door"}]

`add key`
$ curl -X POST http://127.0.0.1:5000/ \
    -H "Content-Type: application/json" \
    -d '{"text":"what flaskapi can do?"}'

use double quotes for json content

`get key=1`
$ curl -X GET http://127.0.0.1:5000/1/
{"url": "http://127.0.0.1:5000/1/", "text": "build the codez"}

`update key=1`
$ curl -X PUT http://127.0.0.1:5000/1/ -d text="flask api is awesomez"
{"url": "http://127.0.0.1:5000/1/", "text": "flask api is teh awesomez"}

$ curl -X PUT http://127.0.0.1:5000/4/ \
    -H "Content-Type: application/json" \
    -d '{"text":"Why is restapi so popular?"}'

`delete key=1`
$ curl -X DELETE http://127.0.0.1:5000/1/


## Example 2 - [File](https://towardsdatascience.com/flask-an-easy-access-door-to-api-development-2147ae694ceb)

`$ curl http://localhost:5000/getJsonFromFile/labelsFile.json`

`curl -F "FILES_LIST=@./file1.txt" -F "FILES_LIST=@./file 2.txt" -F "DIR_NAME=uploads" localhost:5000/uploadFiles`


## Example 3 - Python REST APIs With Flask, Connexion, and SQLAlchemy
- [part-1](https://realpython.com/flask-connexion-rest-api/)
- [part-2](https://realpython.com/flask-connexion-rest-api-part-2/)
- [part-3](https://realpython.com/flask-connexion-rest-api-part-3/)
- [part-4](https://realpython.com/flask-connexion-rest-api-part-4/)

realpython/materials/flask-connexion-rest

curl -X GET http://0.0.0.0:5000/api/people

Swagger UI: localhost:5000/api/ui

```
pip install connexion
pip install swagger-ui-bundle  # for swagger-ui
pip install "connexion[swagger-ui]"

pip install Flask-SQLAlchemy flask-marshmallow marshmallow-sqlalchemy marshmallow

pip install connexion-compose
```

open URL= https://editor.swagger.io/

File > Import swagger.yml

Generate Server > python-flask

Generate Client > python

add logic to realpython-flask-rest/people-v3/python-flask-server/swagger_server/controllers/people_controller.pypython-flask-server/swagger_server/controllers/people_controller.py

1) run python-flask-server (generated)
`$ python3 -m swagger_server`

2) use Swagger UI client
open url = http://localhost:8080/api/ui/

3) use python-client (generated)
```
$ cd ~/projects/flaskapi/realpython-flask-rest/people-v3/python-client
$ pip install -e .  # install swagger-client
$ ipython
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

try:
    # Read the entire list of people
    api_response = api_instance.people_read_all(length=length, offset=offset)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PeopleApi->people_read_all: %s\n" % e)

import requests
resp = requests.get('http://0.0.0.0:8080/api/people')
resp.status_code, resp.text

```


### part-3
```
cd realpython/materials/flask-connexion-rest-part-3
virtualenv flaskp3
source flaskp3/bin/activate
pip install -r requirements.txt
python build_database.py
python server.py

```





## References

### [How to Build an API in Python (with Flask & RapidAPI)](https://rapidapi.com/blog/how-to-build-an-api-in-python/)


### [httpie](https://www.tecmint.com/httpie-http-client-for-linux/) 

A Modern HTTP Client Similar to Curl and Wget Commands

http http://127.0.0.1:5000/1/
http http://127.0.0.1:5000/
http POST http://127.0.0.1:5000/ text="what is pytest-bdd"
