# https://requests-oauthlib.readthedocs.org/en/latest/examples/real_world_example.html#real-example

import os

from requests_oauthlib import OAuth1Session
from flask import Flask, request, redirect, session, url_for
from flask.json import jsonify

from settings import EVERNOTE_CONSUMER_KEY, EVERNOTE_CONSUMER_SECRET

app = Flask(__name__)

# Evernote key/secret

client_id = EVERNOTE_CONSUMER_KEY
client_secret = EVERNOTE_CONSUMER_SECRET

request_token_url = 'https://sandbox.evernote.com/oauth'
authorization_base_url = 'https://sandbox.evernote.com/OAuth.action'
access_token_url = 'https://sandbox.evernote.com/oauth'

callback_uri = 'http://localhost:5000/callback'

@app.route("/")
def demo():
    """Step 1: User Authorization.

    Redirect the user/resource owner to the OAuth provider (i.e. Github)
    using an URL with a few key OAuth parameters.   
    """
    
    evernote = OAuth1Session(client_id, client_secret=client_secret,
         callback_uri=callback_uri)
    fetch_response = evernote.fetch_request_token(request_token_url)

    authorization_url = evernote.authorization_url(authorization_base_url)
    session['resource_owner_key'] = fetch_response.get('oauth_token')
    session['resource_owner_secret'] = fetch_response.get('oauth_token_secret')

    return redirect(authorization_url)


# Step 2: User authorization, this happens on the provider.

@app.route("/callback", methods=["GET"])
def callback():
    """ Step 3: Retrieving an access token.

    The user has been redirected back from the provider to your registered
    callback URL. With this redirection comes an authorization code included
    in the redirect URL. We will use that to obtain an access token.
    """

    resource_owner_key = str(session.get('resource_owner_key'))
    resource_owner_secret = str(session.get('resource_owner_secret'))
    
    #return (resource_owner_key + "|" + resource_owner_secret)
    
    evernote = OAuth1Session(client_key = client_id,
                          client_secret = client_secret,
                          resource_owner_key = resource_owner_key,
                          resource_owner_secret = resource_owner_secret)
                          
    oauth_response = evernote.parse_authorization_response(request.url)
    
    token_dict = evernote.fetch_access_token(access_token_url)

    # At this point you can fetch protected resources but lets save
    # the token and show how this is done from a persisted token
    # in /profile.
    session['oauth_token'] = token_dict['oauth_token']

    return redirect(url_for('.profile'))


@app.route("/profile", methods=["GET"])
def profile():
    """Fetching a protected resource using an OAuth 1 token.
    """
    
    import hashlib
    import binascii
    import evernote.edam.userstore.constants as UserStoreConstants
    import evernote.edam.type.ttypes as Types

    from evernote.api.client import EvernoteClient

    auth_token = session['oauth_token']
    client = EvernoteClient(token=auth_token, sandbox=True)
    
    user_store = client.get_user_store()
    
    version_ok = user_store.checkVersion(
        "Evernote EDAMTest (Python)",
        UserStoreConstants.EDAM_VERSION_MAJOR,
        UserStoreConstants.EDAM_VERSION_MINOR
    )

    note_store = client.get_note_store()
    
    # List all of the notebooks in the user's account
    notebooks = note_store.listNotebooks()
    return ", " .join([notebook.name for notebook in notebooks])
    

if __name__ == "__main__":
    # This allows us to use a plain HTTP callback
    os.environ['DEBUG'] = "1"

    app.secret_key = os.urandom(24)
    app.run(debug=True)


