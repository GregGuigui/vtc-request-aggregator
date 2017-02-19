from collections import namedtuple
from yaml import safe_load

from uber_rides.client import UberRidesClient
from uber_rides.session import OAuth2Credential
from uber_rides.session import Session


# set your app credentials here
CREDENTIALS_FILENAME = './config.yml'

# where your OAuth 2.0 credentials are stored
STORAGE_FILENAME = 'oauth2_session_store.yml'

DEFAULT_CONFIG_VALUES = frozenset([
    'INSERT_CLIENT_ID_HERE',
    'INSERT_CLIENT_SECRET_HERE',
    'INSERT_REDIRECT_URL_HERE',
])

def import_app_credentials(filename=CREDENTIALS_FILENAME):
    """Import app credentials from configuration file.
    Parameters
        filename (str)
            Name of configuration file.
    Returns
        credentials (dict)
            All your app credentials and information
            imported from the configuration file.
    """
    with open(filename, 'r') as config_file:
        config = safe_load(config_file)

    client_id = config['client_id']
    client_secret = config['client_secret']
    redirect_url = config['redirect_url']

    config_values = [client_id, client_secret, redirect_url]

    for value in config_values:
        if value in DEFAULT_CONFIG_VALUES:
            exit('Missing credentials in {}'.format(filename))

    credentials = {
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_url': redirect_url,
        'scopes': set(config['scopes']),
    }

    return credentials


def import_oauth2_credentials(filename=STORAGE_FILENAME):
    """Import OAuth 2.0 session credentials from storage file.
    Parameters
        filename (str)
            Name of storage file.
    Returns
        credentials (dict)
            All your app credentials and information
            imported from the configuration file.
    """
    with open(filename, 'r') as storage_file:
        storage = safe_load(storage_file)

    # depending on OAuth 2.0 grant_type, these values may not exist
    client_secret = storage.get('client_secret')
    redirect_url = storage.get('redirect_url')
    refresh_token = storage.get('refresh_token')

    credentials = {
        'access_token': storage['access_token'],
        'client_id': storage['client_id'],
        'client_secret': client_secret,
        'expires_in_seconds': storage['expires_in_seconds'],
        'grant_type': storage['grant_type'],
        'redirect_url': redirect_url,
        'refresh_token': refresh_token,
        'scopes': storage['scopes'],
    }

    return credentials


def create_uber_client(credentials):
    """Create an UberRidesClient from OAuth 2.0 credentials.
    Parameters
        credentials (dict)
            Dictionary of OAuth 2.0 credentials.
    Returns
        (UberRidesClient)
            An authorized UberRidesClient to access API resources.
    """
    oauth2credential = OAuth2Credential(
        client_id=credentials.get('client_id'),
        access_token=credentials.get('access_token'),
        expires_in_seconds=credentials.get('expires_in_seconds'),
        scopes=credentials.get('scopes'),
        grant_type=credentials.get('grant_type'),
        redirect_url=credentials.get('redirect_url'),
        client_secret=credentials.get('client_secret'),
        refresh_token=credentials.get('refresh_token'),
    )
    session = Session(oauth2credential=oauth2credential)
    return UberRidesClient(session, sandbox_mode=True)

