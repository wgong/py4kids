## Web identity: OAuth2 and OpenIDConnect
- Brendan McCollam
- University of Chicago / Globus
- Slides and code: http://brendan.mccoll.am/pycon2017


To run these examples:

### I suggest creating a virtual envionment to install libraries
   http://docs.python-guide.org/en/latest/dev/virtualenvs/

   Run:
   `virtualenv globus`
   `source ./globus/bin/activate`

### Install required dependencies
   https://pip.pypa.io/en/stable/reference/pip_install/

   Run:
  `pip install -r requirements.txt`

### For the oidc_login.py and oauth2_login.py examples
   you'll need to register your application with an
   authorization provider, and fill out the CONFIG
   dictionary in the file.

   If you want to use Globus, you can go to
   https://developers.globus.org/ to register your
   app.

   For other providers (Google, Facebook, etc.)  see
   their docs.


### Set flask to run a particular example, and launch it
   http://flask.pocoo.org/docs/0.12/quickstart/

   Run:
   `export FLASK_APP=oauth2_login.py; flask run`

Depending on your local setup, you may need to set up a
reverse-proxy to support SSL requests.
This doc might help:
https://www.digitalocean.com/community/tutorials/how-to-configure-nginx-with-ssl-as-a-reverse-proxy-for-jenkins


### install SQLite Browser
https://linuxhint.com/install-sqlite-browser-ubuntu/

- install
   sudo add-apt-repository ppa:linuxgndu/sqlitebrowser-testing
   sudo apt-get update && sudo apt-get install sqlitebrowser

- uninstall
   sudo apt-get remove sqlitebrowser

how to add another user

ipython:
```
   from passlib.hash import bcrypt
   pw_hash = bcrypt.hash("wengong")
```
`$ sqlitebrowser test.db`

SQL:
`insert into user(id,username,password_hash) values(2,'wengong',pw_hash)`


### add-https-functionality-to-a-python-flask-web-server
https://stackoverflow.com/questions/29458548/can-you-add-https-functionality-to-a-python-flask-web-server

`$ pip install pyopenssl`

create 'cert.pem' and 'key.pem' 
`$ openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365`

password login method:
=========================
   `export FLASK_APP=password_login.py; flask run`
   or 
   `python password_login.py`

OAuth2 login method:
====================
   `export FLASK_APP=oauth2_login.py; flask run`
   or 
   `python oauth2_login.py`

OIDC login method:
====================
   `export FLASK_APP=oidc_login.py; flask run`
   or 
   `python oidc_login.py`

