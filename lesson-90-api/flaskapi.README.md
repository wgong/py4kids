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



















### [httpie](https://www.tecmint.com/httpie-http-client-for-linux/) 

A Modern HTTP Client Similar to Curl and Wget Commands

http http://127.0.0.1:5000/1/
http http://127.0.0.1:5000/
http POST http://127.0.0.1:5000/ text="what is pytest-bdd"
