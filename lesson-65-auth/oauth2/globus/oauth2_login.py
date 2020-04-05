import json
from flask import (Flask, redirect, url_for,
    request, session, render_template)
from requests_oauthlib import OAuth2Session
import requests
from urllib import parse
from datetime import datetime

import configuration as cfg
import utils

app = Flask(__name__)
app.secret_key = "keep this secret"



@app.route('/login', methods=['GET'])
def login():
    provider = OAuth2Session(
                   client_id=cfg.CONFIG['client_id'],
                   scope=cfg.CONFIG['scope'],
                   redirect_uri=cfg.CONFIG['redirect_uri'])
    url, state = provider.authorization_url(cfg.CONFIG['auth_url'])
    # print(f"url: {url}\nstate: {state}")
    session['oauth2_state'] = state
    return redirect(url)

@app.route('/callback', methods=['GET'])
def callback():
    provider = OAuth2Session(cfg.CONFIG['client_id'],
                             redirect_uri=cfg.CONFIG['redirect_uri'],
                             state=session['oauth2_state'])
    # print(f"request.url= {request.url}")
    qparams = parse.parse_qs(parse.urlparse(request.url).query)
    session['code'] = qparams['code'][0]
    session['state'] = qparams['state'][0]
    # print(f"code: {qparams['code'][0]}")
    # print(f"state: {qparams['state'][0]}")
    token_response = provider.fetch_token(
                        token_url=cfg.CONFIG['token_url'],
                        client_secret=cfg.CONFIG['client_secret'],
                        authorization_response=request.url)

    session['access_token'] = token_response['access_token']
    expires_date = datetime.utcfromtimestamp(token_response['expires_at']).strftime('%Y-%m-%d %H:%M:%S')
    session['access_token_expires'] = expires_date
    # print(f"access token: {session['access_token']}\nexpires at {expires_date}")

    return redirect(url_for('index'))

@app.route('/')
def index():
    if 'access_token' not in session:
        return redirect(url_for('login'))
    transfers = requests.get(cfg.CONFIG['task_list_url'],
                             headers={'Authorization': 'Bearer ' + session['access_token']})

    info_dict = dict(
        code=session['code'],
        access_token=session['access_token'],
        access_token_expires=session['access_token_expires'],
    )
    return render_template('index.html.jinja2',
                idp_provider_url=cfg.CONFIG['idp_provider_url'],
                info=json.dumps(info_dict),
                transfers=str(transfers.json())
            )

if __name__ == '__main__':
    proto, host, port, path = utils.parse_url(cfg.CONFIG['redirect_uri'])
    print(proto, host, port, path)

    if proto == "https":
        app.run(host=host, port=int(port), debug=True, 
            ssl_context=('cert.pem', 'key.pem'))
    else:
        app.run(host=host, port=int(port), debug=True)