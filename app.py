from flask import Flask, redirect, request, jsonify, session, url_for, render_template
from yaml import safe_dump
from uber_rides.client import UberRidesClient
from uber_rides.session import OAuth2Credential
from uber_rides.session import Session
from middlewares.auth import get_uber_session
import authorize_user
import utils

app = Flask(__name__)
app.debug = True
app.secret_key = 'GregGuiCle'

app.credentials = credentials = utils.import_app_credentials("config.yml")
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
    return redirect(url_for('dashboard'))

@app.route("/dashboard")
def dashboard():
    return render_template('dashboard.html')

@app.route("/api/uber/activity")
def activity():
    uber_session = get_uber_session(credentials)
    uber_client = UberRidesClient(uber_session, sandbox_mode=True)
    response = uber_client.get_user_activity()
    history = response.json

    return jsonify(history)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)
