from flask import session, request, g
from uber_rides.session import OAuth2Credential, Session
from uber_rides.client import UberRidesClient
from lyft_rides.client import LyftRidesClient

from app import app, env
from app.db import User
from services.uber_authorize_user import credentials as uber_credentials
from services.lyft_authorize_user import credentials as lyft_credentials

@app.before_request
def get_vtc_session():
    user_id = session.get('user_id')
    
    if user_id is None:
        return
    
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return
    
    # if oauth2credential is None:
    #     return false
    if user.uber_access_token is not None:
        uber_oauth2credentials = OAuth2Credential(
            client_id=uber_credentials['client_id'],
            scopes=uber_credentials['scopes'],
            redirect_url=uber_credentials['redirect_url'],
            client_secret=uber_credentials['client_secret'],
            access_token=user.uber_access_token,
            refresh_token=user.uber_refresh_token,
            expires_in_seconds=user.uber_expires_in_seconds,
            grant_type=user.uber_grant_type)
    
        g.uber_session = Session(oauth2credential=uber_oauth2credentials)
        g.uber_client = UberRidesClient(g.uber_session, sandbox_mode=(env != 'prod'))
    
    if user.lyft_access_token is not None:
        lyft_oauth2credentials = OAuth2Credential(
            client_id=lyft_credentials['client_id'],
            scopes=lyft_credentials['scopes'],
            redirect_url=lyft_credentials['redirect_url'],
            client_secret=lyft_credentials['client_secret'],
            access_token=user.lyft_access_token,
            refresh_token=user.lyft_refresh_token,
            expires_in_seconds=user.lyft_expires_in_seconds,
            grant_type=user.lyft_grant_type)
    
        g.lyft_session = Session(oauth2credential=lyft_oauth2credentials)
        g.lyft_client = LyftRidesClient(g.lyft_session)

