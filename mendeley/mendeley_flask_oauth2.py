# https://requests-oauthlib.readthedocs.org/en/latest/examples/real_world_example.html#real-example
# need to run
#     OAUTHLIB_INSECURE_TRANSPORT=1 python MENDELEY_flask_oauth2.py
# (if without SSL)

from requests_oauthlib import OAuth2Session
from flask import Flask, request, redirect, session, url_for
from flask.json import jsonify
import os

# pick up keys from env
MENDELEY_CONSUMER_KEY = os.environ.get('MENDELEY_CONSUMER_KEY')
MENDELEY_CONSUMER_SECRET = os.environ.get('MENDELEY_CONSUMER_SECRET')
MENDELEY_REDIRECT_URI = os.environ.get('MENDELEY_REDIRECT_URI')

app = Flask(__name__)

# This information is obtained upon registration of a new MENDELEY OAuth
# application here: https://MENDELEY.com/settings/applications/new
# https://MENDELEY.com/settings/applications/261763
client_id = MENDELEY_CONSUMER_KEY
client_secret = MENDELEY_CONSUMER_SECRET
redirect_uri = MENDELEY_REDIRECT_URI

authorization_base_url = 'https://api.mendeley.com/oauth/authorize'
token_url = 'https://api.mendeley.com/oauth/token'
default_scopes = ['all']


@app.route("/")
def demo():
    """Step 1: User Authorization.

    Redirect the user/resource owner to the OAuth provider (i.e. MENDELEY)
    using an URL with a few key OAuth parameters.
    """

    mendeley = OAuth2Session(client_id, scope=default_scopes, redirect_uri=redirect_uri)
    authorization_url, state = mendeley.authorization_url(authorization_base_url)

    # State is used to prevent CSRF, keep this for later.
    session['oauth_state'] = state

    return redirect(authorization_url)


# Step 2: User authorization, this happens on the provider.

@app.route("/callback", methods=["GET"])
def callback():
    """ Step 3: Retrieving an access token.

    The user has been redirected back from the provider to your registered
    callback URL. With this redirection comes an authorization code included
    in the redirect URL. We will use that to obtain an access token.
    """

    mendeley = OAuth2Session(client_id, redirect_uri=redirect_uri,
          state=session['oauth_state'])
    token = mendeley.fetch_token(token_url, client_secret=client_secret,
                               authorization_response=request.url)

    # At this point you can fetch protected resources but lets save
    # the token and show how this is done from a persisted token
    # in /profile.
    session['oauth_token'] = token

    return redirect(url_for('.profile'))


@app.route("/profile", methods=["GET"])
def profile():
    """Fetching a protected resource using an OAuth 2 token.
    """

    return ("Success")



if __name__ == "__main__":
    # This allows us to use a plain HTTP callback
    os.environ['DEBUG'] = "1"

    app.secret_key = os.urandom(24)
    app.run(host="0.0.0.0", debug=True, port=5000)
    #app.run(debug=True, port=5000)
