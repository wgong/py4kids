CONFIG = {
    # IdP name
    'idp_provider_url': 'https://www.facebook.com/',

    # configuration for oauth2_login.py
    'client_id': "1234567890123456789",
    'client_secret': "da0dc41caaaaaaaa99b1f45d1ea3e272737a",
    'auth_url': 'https://www.facebook.com/dialog/oauth',
    'token_url': 'https://graph.facebook.com/v2.2/oauth/access_token',
    'scope': ['ads_management'],
    'redirect_uri': 'http://localhost:8080/',

}
