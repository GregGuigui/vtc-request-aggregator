from flask import session
from uber_rides.session import OAuth2Credential, Session

def get_uber_session(credentials):
    oauth2credential = session.get('tokens')
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

    uber_session = Session(oauth2credential=uber_credentials)
    return uber_session
