from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from yaml import safe_dump

import utils
from utils import import_app_credentials

from uber_rides.auth import AuthorizationCodeGrant
from uber_rides.client import UberRidesClient
from uber_rides.errors import ClientError
from uber_rides.errors import ServerError
from uber_rides.errors import UberIllegalState
import utils

def get_auth_flow(credentials):
    return AuthorizationCodeGrant(
        credentials.get('client_id'),
        credentials.get('scopes'),
        credentials.get('client_secret'),
        credentials.get('redirect_url'),
    )

def authorization_code_grant_flow(auth_flow):
    """Get an access token through Authorization Code Grant.
    Parameters
        credentials (dict)
            All your app credentials and information
            imported from the configuration file.
        storage_filename (str)
            Filename to store OAuth 2.0 Credentials.
    Returns
        (UberRidesClient)
            An UberRidesClient with OAuth 2.0 Credentials.
    """
    
    auth_url = auth_flow.get_authorization_url()

    return auth_url

def handle_callback(auth_flow, callback_url):
    try:
        session = auth_flow.get_session(callback_url)

    except (ClientError, UberIllegalState) as error:
        return error

    return session.oauth2credential
    # credential_data = {
    #     'client_id': credential.client_id,
    #     'redirect_url': credential.redirect_url,
    #     'access_token': credential.access_token,
    #     'expires_in_seconds': credential.expires_in_seconds,
    #     'scopes': list(credential.scopes),
    #     'grant_type': credential.grant_type,
    #     'client_secret': credential.client_secret,
    #     'refresh_token': credential.refresh_token,
    # }

    # with open(utils.CREDENTIALS_FILENAME, 'w') as yaml_file:
    #     yaml_file.write(safe_dump(credential_data, default_flow_style=False))

    # return UberRidesClient(session, sandbox_mode=True)