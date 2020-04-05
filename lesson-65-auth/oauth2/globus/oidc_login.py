from random import SystemRandom
import json
from flask import (Flask, redirect, url_for,
    request, session, render_template)
from requests_oauthlib import OAuth2Session
import requests
from urllib import parse
from datetime import datetime
from jose import jwt
import configuration as cfg
import utils

random = SystemRandom()


keys = requests.get('https://auth.globus.org/jwk.json').json()

OIDC_CONFIG = {
    'jwt_pubkeys': keys,
    'scope': ['openid', 'email', 'profile'],
    'expected_issuer': 'https://auth.globus.org',
    'algorithm': 'RS512'
}

cfg.CONFIG.update(OIDC_CONFIG)

# USER_CONFIG = {
#     'client_identity_username': f"{cfg.CONFIG['client_id']}@clients.auth.globus.org"
# }
# cfg.CONFIG.update(USER_CONFIG)
# print(f"client_identity_username: {cfg.CONFIG.get('client_identity_username')}")

app = Flask(__name__)
app.secret_key = "keep this secret"

@app.route('/login', methods=['GET'])
def login():
    provider = OAuth2Session(client_id=cfg.CONFIG['client_id'],
                             scope=cfg.CONFIG['scope'],
                             redirect_uri=cfg.CONFIG['redirect_uri'])
    nonce = str(random.randint(0, 1e10))

    url, state = provider.authorization_url(cfg.CONFIG['auth_url'],
                                            nonce=nonce)
    session['oauth2_state'] = state
    session['nonce'] = nonce
    return redirect(url)


@app.route('/callback', methods=['GET'])
def callback():
    provider = OAuth2Session(cfg.CONFIG['client_id'],
                             redirect_uri=cfg.CONFIG['redirect_uri'],
                             state=session['oauth2_state'])

    qparams = parse.parse_qs(parse.urlparse(request.url).query)
    session['code'] = qparams['code'][0]
    session['state'] = qparams['state'][0]
    
    response = provider.fetch_token(
                         token_url=cfg.CONFIG['token_url'],
                         client_secret=cfg.CONFIG['client_secret'],
                         authorization_response=request.url)
    session['access_token'] = response['access_token']
    id_token = response['id_token']
    claims = jwt.decode(id_token,
                        key=cfg.CONFIG['jwt_pubkeys'],
                        issuer=cfg.CONFIG['expected_issuer'],
                        audience=cfg.CONFIG['client_id'],
                        algorithms=cfg.CONFIG['algorithm'],
                        access_token=response['access_token'])
    assert session['nonce'] == claims['nonce']
    session['id_token'] = id_token
    session['user_id'] = claims['sub']
    session['user_email'] = claims['email']
    session['user_name'] = claims['name']
    return redirect(url_for('index'))

@app.route('/')
def index():
    if 'access_token' not in session:
        return redirect(url_for('login'))
    info_dict = dict(
        code=session['code'],
        access_token=session['access_token'],
        id_token=session['id_token'],
        user_id=session['user_id'],
        user_email=session['user_email'],
        user_name=session['user_name'],
        nonce=session['nonce'],
    )
    return render_template('index.html.jinja2',
            idp_provider_url=cfg.CONFIG['idp_provider_url'],
            info=json.dumps(info_dict),
        )

if __name__ == '__main__':
    proto, host, port, path = utils.parse_url(cfg.CONFIG['redirect_uri'])
    print(proto, host, port, path)

    if proto == "https":
        app.run(host=host, port=int(port), debug=True, 
            ssl_context=('cert.pem', 'key.pem'))
    else:
        app.run(host=host, port=int(port), debug=True)