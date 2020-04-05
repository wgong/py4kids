"""

# this example is adapted from blog on 2020-04-02
# https://www.pmg.com/blog/logging-facebook-oauth2-via-command-line-using-python/

# Facebook Developer
# https://developers.facebook.com/docs/facebook-login/access-tokens

# when does Facebook Oauth2 Access Token expire? 
https://stackoverflow.com/questions/2687770/do-facebook-oauth-2-0-access-tokens-expire

"""

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.request import urlopen, HTTPError
from webbrowser import open_new
import json

import utils
import configuration as cfg

REDIRECT_URL = cfg.CONFIG['redirect_uri']

class HTTPServerHandler(BaseHTTPRequestHandler):

    """
    HTTP Server callbacks to handle Facebook OAuth redirects
    """
    def __init__(self, request, address, server, client_id, client_secret):
        self._id = client_id
        self._secret = client_secret
        super().__init__(request, address, server)

    def do_GET(self):
        GRAPH_API_AUTH_URI = (cfg.CONFIG['token_url']
            + '?client_id=' + self._id + '&redirect_uri=' 
            + REDIRECT_URL + '&client_secret=' + self._secret + '&code=')

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        if 'code' in self.path:
            self.auth_code = self.path.split('=')[1]
            # print(f"auth_code=\n{self.auth_code}")
            self.wfile.write(bytes('<html><h1>You may now close this window.'
                              + '</h1></html>', 'utf-8'))
            access_token = self.get_access_token_from_url(
                    GRAPH_API_AUTH_URI + self.auth_code)
            self.server.access_token = access_token
            #print(f"access_token={access_token}")       

    # Disable logging from the HTTP Server
    def log_message(self, format, *args):
        return

    def get_access_token_from_url(self, url):
        """
        Parse the access token from Facebook's response
        Args:
            uri: the facebook graph api oauth URI containing valid client_id,
                redirect_uri, client_secret, and auth_code arguements
        Returns:
            a dict containing the access_token 
        """
        return json.loads(str(urlopen(url).read(), 'utf-8'))



class TokenHandler:
    """
    Functions used to handle Facebook oAuth
    """
    def __init__(self, client_id, client_secret):
        self._id = client_id
        self._secret = client_secret

    def get_access_token(self):
        """
         Fetches the access key using an HTTP server to handle oAuth
         requests
            Args:
                appId:      The Facebook assigned App ID
                appSecret:  The Facebook assigned App Secret
        """
        proto, host, port, path = utils.parse_url(REDIRECT_URL)
        ACCESS_URI = (cfg.CONFIG['auth_url']
            + '?client_id=' +self._id + '&redirect_uri='
            + REDIRECT_URL + "&scope=ads_management")
        open_new(ACCESS_URI)
        httpServer = HTTPServer((host, int(port)),
                lambda request, address, server: HTTPServerHandler(
                    request, address, server, self._id, self._secret))
        httpServer.handle_request()
        access_token = httpServer.access_token 
        return access_token

if __name__ == "__main__":
    import os
    th = TokenHandler(cfg.CONFIG['client_id'],cfg.CONFIG['client_secret'])
    at = th.get_access_token()
    print(f"{at['token_type']} access_token: \n\t{at['access_token']} ")
    print(f"will expire in {at['expires_in']/(3600*24):.2f} days")