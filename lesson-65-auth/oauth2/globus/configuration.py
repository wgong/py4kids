CONFIG = {
    # IdP name
    'idp_provider_url': 'https://www.globus.org/',

    # configuration for oauth2_login.py
    'client_id': "abcdefg-1111-a5c3",
    'client_secret': "bfNE1111QLdDxPWITHHNg",
    'auth_url': 'https://auth.globus.org/v2/oauth2/authorize',
    'token_url': 'https://auth.globus.org/v2/oauth2/token',
    'scope': ['urn:globus:auth:scope:transfer.api.globus.org:all'],
    'redirect_uri': 'https://localhost:5000/callback',
    'task_list_url': 'https://transfer.api.globusonline.org/v0.10/task_list?limit=1',

    # configuration for password_login.py
    'user_name': 'brendan',
    'password': 'password',
}
