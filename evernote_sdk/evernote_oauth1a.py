# https://requests-oauthlib.readthedocs.org/en/latest/examples/real_world_example.html#real-example

import os

from flask import Flask, request, redirect, session, url_for
from flask.json import jsonify

# import hashlib
# import binascii
import evernote.edam.userstore.constants as UserStoreConstants
# import evernote.edam.type.ttypes as Types

from evernote.api.client import EvernoteClient

EVERNOTE_CONSUMER_KEY = os.environ.get("EVERNOTE_CONSUMER_KEY")
EVERNOTE_CONSUMER_SECRET = os.environ.get("EVERNOTE_CONSUMER_SECRET")
EVERNOTE_PRODUCTION = os.environ.get("EVERNOTE_PRODUCTION", 'False')  #default to sandbox
EVERNOTE_DEV_AUTH_TOKEN = os.environ.get("EVERNOTE_DEV_AUTH_TOKEN", '')
EVERNOTE_CALLBACK_URI = os.environ.get("EVERNOTE_CALLBACK_URI")

SANDBOX = False if EVERNOTE_PRODUCTION == 'True' else True

app = Flask(__name__)

# Evernote key/secret

BASE_URL = "https://www.evernote.com" if EVERNOTE_PRODUCTION == 'True' \
           else "https://sandbox.evernote.com"

request_token_url = '{}/oauth'.format(BASE_URL)
authorization_base_url = '{}/OAuth.action'.format(BASE_URL)
access_token_url = '{}/oauth'.format(BASE_URL)


# https://github.com/evernote/evernote-sdk-python/blob/1.25.0/sample/django/oauth/views.py#L11
def get_evernote_client(token=None, sandbox=True):
    if token is not None:
        return EvernoteClient(token=token, sandbox=sandbox)
    else:
        return EvernoteClient(
            consumer_key=EVERNOTE_CONSUMER_KEY,
            consumer_secret=EVERNOTE_CONSUMER_SECRET,
            sandbox=sandbox
        )

@app.route("/")
def demo():
    """Step 1: User Authorization.

    Redirect the user/resource owner to the OAuth provider (i.e. Github)
    using an URL with a few key OAuth parameters.
    """

    client = get_evernote_client(token=None, sandbox=SANDBOX)
    request_token = client.get_request_token(EVERNOTE_CALLBACK_URI)

    session['oauth_token'] = request_token['oauth_token']
    session['oauth_token_secret'] = request_token['oauth_token_secret']

    return redirect(client.get_authorize_url(request_token))


# Step 2: User authorization, this happens on the provider.

@app.route("/callback", methods=["GET"])
def callback():
    """ Step 3: Retrieving an access token.

    The user has been redirected back from the provider to your registered
    callback URL. With this redirection comes an authorization code included
    in the redirect URL. We will use that to obtain an access token.
    """

    try:
        client = get_evernote_client(token=None, sandbox=SANDBOX)
        token = client.get_access_token(
            session['oauth_token'],
            session['oauth_token_secret'],
            request.args.get('oauth_verifier', '')
        )
        session['token'] = token
    except Exception as e:
        return str(e)

    return redirect(url_for('.profile'))

@app.route("/profile", methods=["GET"])
def profile():
    """Fetching a protected resource using an OAuth 1 token.
    """

    token = session['token']
    client = get_evernote_client(token=token, sandbox=SANDBOX)

    user_store = client.get_user_store()

    version_ok = user_store.checkVersion(
        "Evernote EDAMTest (Python)",
        UserStoreConstants.EDAM_VERSION_MAJOR,
        UserStoreConstants.EDAM_VERSION_MINOR
    )

    note_store = client.get_note_store()

    # List all of the notebooks in the user's account
    notebooks = note_store.listNotebooks()
    return "<br/>" .join([notebook.name for notebook in notebooks])


if __name__ == "__main__":
    # This allows us to use a plain HTTP callback
    os.environ['DEBUG'] = "1"

    app.secret_key = os.urandom(24)
    app.run(host="0.0.0.0", port=5000, debug=True)
