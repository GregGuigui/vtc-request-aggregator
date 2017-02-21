from flask import session, request, g
from uber_rides.session import OAuth2Credential, Session
from uber_rides.client import UberRidesClient

from app import app, env
from services.uber_credentials import credentials

@app.before_request
def get_uber_session():
    oauth2credential = session.get('tokens')
    
    if oauth2credential is None:
        return
    # if oauth2credential is None:
    #     return false

    uber_credentials = OAuth2Credential(
        client_id=credentials['client_id'],
        access_token=oauth2credential['access_token'],
        expires_in_seconds=oauth2credential['expires_in_seconds'],
        scopes=credentials['scopes'],
        grant_type=oauth2credential['grant_type'],
        redirect_url=credentials['redirect_url'],
        client_secret=credentials['client_secret'],
        refresh_token=oauth2credential['refresh_token'])

    g.uber_session = Session(oauth2credential=uber_credentials)
    g.uber_client = UberRidesClient(g.uber_session, sandbox_mode=(env != 'prod'))
