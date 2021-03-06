# https://requests-oauthlib.readthedocs.org/en/latest/examples/real_world_example.html#real-example
# need to run
#     OAUTHLIB_INSECURE_TRANSPORT=1 python github_flask_oauth2.py
# (if without SSL)

from requests_oauthlib import OAuth2Session
from flask import Flask, request, redirect, session, url_for
from flask.json import jsonify
import os

# pick up keys from env
GITHUB_CONSUMER_KEY = os.environ.get('GITHUB_CONSUMER_KEY')
GITHUB_CONSUMER_SECRET = os.environ.get('GITHUB_CONSUMER_SECRET')
GITHUB_REDIRECT_URI = os.environ.get('GITHUB_REDIRECT_URI')

app = Flask(__name__)

# This information is obtained upon registration of a new GitHub OAuth
# application here: https://github.com/settings/applications/new
# https://github.com/settings/applications/261763
client_id = GITHUB_CONSUMER_KEY
client_secret = GITHUB_CONSUMER_SECRET
redirect_uri = GITHUB_REDIRECT_URI

authorization_base_url = 'https://github.com/login/oauth/authorize'
token_url = 'https://github.com/login/oauth/access_token'


@app.route("/")
def demo():
    """Step 1: User Authorization.

    Redirect the user/resource owner to the OAuth provider (i.e. Github)
    using an URL with a few key OAuth parameters.
    """

    github = OAuth2Session(client_id, redirect_uri=redirect_uri)
    authorization_url, state = github.authorization_url(authorization_base_url)

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

    github = OAuth2Session(client_id, state=session['oauth_state'])
    token = github.fetch_token(token_url, client_secret=client_secret,
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
    github = OAuth2Session(client_id, token=session['oauth_token'])
    return jsonify(github.get('https://api.github.com/user').json())


if __name__ == "__main__":
    # This allows us to use a plain HTTP callback
    os.environ['DEBUG'] = "1"

    app.secret_key = os.urandom(24)
    app.run(host="0.0.0.0", debug=True, port=5000)
    #app.run(debug=True, port=5000)
