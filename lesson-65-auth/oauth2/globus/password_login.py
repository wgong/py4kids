from flask import (Flask, redirect, url_for,
    request, session, render_template)
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import bcrypt
import configuration as cfg

app = Flask(__name__)
# This test database contains one user, 'brendan'
# with password 'password'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.secret_key = "keep this secret"
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    password_hash = db.Column(db.String)

@app.route('/')
def index():
    if 'authed_user' not in session:
        return redirect(url_for('login_get'))
    return render_template('index.html.jinja2',
            user_name=session['authed_user']
            #user_name=cfg.CONFIG['user_name'],
            #password=cfg.CONFIG['password'],
        )


@app.route('/login', methods=['GET'])
def login_get():
    return render_template('login.html.jinja2', )


@app.route('/login', methods=['POST'])
def login_post():
    un = request.form['username']
    user = (User.query
                .filter_by(username=un)
                .one())
    pw = request.form['password']
    if bcrypt.verify(pw, user.password_hash):
        session['authed_user'] = user.username
        return redirect(url_for('index'))
    else:
        return "Login error."

if __name__ == '__main__':
    app.run(host="localhost", port=8080, debug=True)