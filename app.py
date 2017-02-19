from flask import Flask, redirect, request, jsonify, session, url_for, render_template
from yaml import safe_dump
from uber_rides.client import UberRidesClient
from uber_rides.session import OAuth2Credential
from uber_rides.session import Session
import authorize_user
import utils

app = Flask(__name__)
app.debug = True
app.secret_key = 'GregGuiCle'

credentials = utils.import_app_credentials("config.yml")
auth_flow = authorize_user.get_auth_flow(credentials)
url = authorize_user.authorization_code_grant_flow(auth_flow)

@app.route("/login")
def login():
    return render_template('index.html')

@app.route("/api/uber/login")
def login_uber():
    return redirect(url)

@app.route("/api/uber/oauth", methods = ["GET"])
def callback():
    oauth2credentials = authorize_user.handle_callback(auth_flow, request.url)
    cred_json = {
        'access_token': oauth2credentials.access_token,
        'refresh_token': oauth2credentials.refresh_token,
        'expires_in_seconds': oauth2credentials.expires_in_seconds,
        'grant_type': oauth2credentials.grant_type
    }
    session['tokens'] = cred_json
    return redirect(url_for('activity'))

@app.route("/api/uber/activity")
def activity():
    oauth2credential = session.get('tokens')
    if oauth2credential is None:
        return redirect(url_for('login'))
    
    uber_credentials = OAuth2Credential(
        client_id = credentials['client_id'],
        access_token = oauth2credential['access_token'],
        expires_in_seconds = oauth2credential['expires_in_seconds'],
        scopes = credentials['scopes'],
        grant_type = oauth2credential['grant_type'],
        redirect_url = credentials['redirect_url'],
        client_secret = credentials['client_secret'],
        refresh_token = oauth2credential['refresh_token'])

    uber_session = Session(oauth2credential = uber_credentials)
    uber_client = UberRidesClient(uber_session, sandbox_mode = True)
    response = uber_client.get_user_activity()
    history = response.json

    return jsonify(history)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)
