from flask import session

from services.uber_authorize_user import get_url as get_uber_url, get_auth_flow as get_uber_auth_flow, handle_callback as uber_handle_callback
from services.lyft_authorize_user import get_url as get_lyft_url, get_auth_flow as get_lyft_auth_flow, handle_callback as lyft_handle_callback

def get_oauth_url(vtc_name):
    method_name = 'get_' + vtc_name + '_url'
    possibles = globals().copy()
    possibles.update(locals())
    method = possibles.get(method_name)
    if not method:
         raise NotImplementedError("Method %s not implemented" % method_name)

    url = method()
    
    return url

def get_credentials(vtc_name, url):
    auth_flow_method_name = 'get_' + vtc_name + '_auth_flow'
    possibles = globals().copy()
    possibles.update(locals())
    auth_flow_method = possibles.get(auth_flow_method_name)
    if not auth_flow_method:
         raise NotImplementedError("Method %s not implemented" % auth_flow_method_name)
         
    handle_callback_name = vtc_name + '_handle_callback'
    possibles = globals().copy()
    possibles.update(locals())
    handle_callback_method = possibles.get(handle_callback_name)
    if not handle_callback_method:
         raise NotImplementedError("Method %s not implemented" % handle_callback_name)

    oauth2credentials = handle_callback_method(auth_flow_method(session[vtc_name + '_state_token']), url)
    return oauth2credentials