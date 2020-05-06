## https://github.com/golang/oauth2/ repo 
has OAuth 2.0 endpoint for many popular oauth2 IdP such as

// Endpoint is Facebook's OAuth 2.0 endpoint.
var Endpoint = oauth2.Endpoint{
	AuthURL:  "https://www.facebook.com/v3.2/dialog/oauth",
	TokenURL: "https://graph.facebook.com/v3.2/oauth/access_token",
}

// Endpoint is Google's OAuth 2.0 endpoint.
var Endpoint = oauth2.Endpoint{
	AuthURL:   "https://accounts.google.com/o/oauth2/auth",
	TokenURL:  "https://oauth2.googleapis.com/token",
	AuthStyle: oauth2.AuthStyleInParams,
}

// Endpoint is Github's OAuth 2.0 endpoint.
var Endpoint = oauth2.Endpoint{
	AuthURL:  "https://github.com/login/oauth/authorize",
	TokenURL: "https://github.com/login/oauth/access_token",
}

// Endpoint is Yahoo's OAuth 2.0 endpoint.
// See https://developer.yahoo.com/oauth2/guide/
var Endpoint = oauth2.Endpoint{
	AuthURL:  "https://api.login.yahoo.com/oauth2/request_auth",
	TokenURL: "https://api.login.yahoo.com/oauth2/get_token",
}

// Endpoint is Uber's OAuth 2.0 endpoint.
var Endpoint = oauth2.Endpoint{
	AuthURL:  "https://login.uber.com/oauth/v2/authorize",
	TokenURL: "https://login.uber.com/oauth/v2/token",
}

// Okta endpoint
{
  "web": {
    "client_id": "1234567890123zieX4x6",
    "client_secret": "1234567890123zieX4x6tYm1234567890123zieX4x68",
    "auth_uri": "https://dev-112233.okta.com/oauth2/default/v1/authorize",
    "token_uri": "https://dev-112233.okta.com/oauth2/default/v1/token",
    "issuer": "https://dev-112233.okta.com/oauth2/default",
    "userinfo_uri": "https://dev-112233.okta.com/oauth2/default/userinfo",
    "redirect_uris": [
      "http://localhost:5000/oidc/callback"
    ],
    "okta_org_url" :  "https://dev-112233.okta.com",
    "okta_auth_token" : "1234567890123zieX4x6tYm12345u0g"
  }
}

## oauth2l
`oauth2l` (pronounced "oauth tool") is a simple command-line tool for
working with
[Google OAuth 2.0](https://developers.google.com/identity/protocols/OAuth2)
written in Go. Its primary use is to fetch and print OAuth 2.0 access
tokens, which can be used with other command-line tools and shell scripts.

## FlaskAPI
~/projects/oauth2/okta/FlaskAPI/app.py