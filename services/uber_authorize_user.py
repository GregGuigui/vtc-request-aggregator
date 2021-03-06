from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from yaml import safe_dump
from flask import session
from app import app, env

from services.utils import import_app_credentials

from uber_rides.auth import AuthorizationCodeGrant
from uber_rides.client import UberRidesClient
from uber_rides.errors import ClientError
from uber_rides.errors import ServerError
from uber_rides.errors import UberIllegalState

credentials = import_app_credentials("app/config/config_uber." + env + ".yml")

def get_url():
    auth_flow = get_auth_flow()
    session['uber_state_token'] = auth_flow.state_token
    uber_url = authorization_code_grant_flow(auth_flow)
    return uber_url

def get_auth_flow(state_token=None):
    return AuthorizationCodeGrant(
        credentials.get('client_id'),
        credentials.get('scopes'),
        credentials.get('client_secret'),
        credentials.get('redirect_url'),
        state_token
    )

def authorization_code_grant_flow(auth_flow):
    auth_url = auth_flow.get_authorization_url()
    return auth_url

def handle_callback(auth_flow, callback_url):
    session = auth_flow.get_session(callback_url)
    return session.oauth2credential