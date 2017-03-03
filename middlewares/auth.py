from flask import session, request, g
from uber_rides.session import OAuth2Credential, Session
from uber_rides.client import UberRidesClient
from lyft_rides.client import LyftRidesClient

from app import app, env
from services.uber_credentials import credentials as uber_credentials
from services.lyft_credentials import credentials as lyft_credentials

@app.before_request
def get_vtc_session():
    tokens = session.get('tokens')
    
    if tokens is None:
        return
    # if oauth2credential is None:
    #     return false
    if 'uber' in tokens:
        uber_oauth2credential_infos = tokens['uber']
        uber_oauth2credentials = OAuth2Credential(
            client_id=uber_credentials['client_id'],
            access_token=uber_oauth2credential_infos['access_token'],
            expires_in_seconds=uber_oauth2credential_infos['expires_in_seconds'],
            scopes=uber_credentials['scopes'],
            grant_type=uber_oauth2credential_infos['grant_type'],
            redirect_url=uber_credentials['redirect_url'],
            client_secret=uber_credentials['client_secret'],
            refresh_token=uber_oauth2credential_infos['refresh_token'])
    
        g.uber_session = Session(oauth2credential=uber_oauth2credentials)
        g.uber_client = UberRidesClient(g.uber_session, sandbox_mode=(env != 'prod'))
    
    if 'lyft' in tokens:
        lyft_oauth2credential_infos = tokens['lyft']
        lyft_oauth2credentials = OAuth2Credential(
            client_id=lyft_credentials['client_id'],
            access_token=lyft_oauth2credential_infos['access_token'],
            expires_in_seconds=lyft_oauth2credential_infos['expires_in_seconds'],
            scopes=lyft_credentials['scopes'],
            grant_type=lyft_oauth2credential_infos['grant_type'],
            redirect_url=lyft_credentials['redirect_url'],
            client_secret=lyft_credentials['client_secret'],
            refresh_token=lyft_oauth2credential_infos['refresh_token'])
    
        g.lyft_session = Session(oauth2credential=lyft_oauth2credentials)
        g.lyft_client = LyftRidesClient(g.lyft_session)

