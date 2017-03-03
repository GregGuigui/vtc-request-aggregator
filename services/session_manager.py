from flask import session, request, g

def create_session(db_user):
    cred_json = {}
    
    if(db_user.uber_access_token is not None):
        cred_json['uber']={
            'access_token': db_user.uber_access_token,
            'refresh_token': db_user.uber_refresh_token,
            'expires_in_seconds': db_user.uber_expires_in_seconds,
            'grant_type': db_user.uber_grant_type
        }
    
    if(db_user.lyft_access_token is not None):
        cred_json['lyft']={
            'access_token': db_user.lyft_access_token,
            'refresh_token': db_user.lyft_refresh_token,
            'expires_in_seconds': db_user.lyft_expires_in_seconds,
            'grant_type': db_user.lyft_grant_type
        }
    
    cred_json['user_id'] = db_user.id
    session['tokens'] = cred_json