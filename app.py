from flask import Flask, redirect, request, jsonify, session, url_for, render_template
from yaml import safe_dump
from uber_rides.client import UberRidesClient
from uber_rides.session import OAuth2Credential
from uber_rides.session import Session
from middlewares.auth import get_uber_session

import os
import authorize_user
import utils

app = Flask(__name__)
app.debug = True
app.secret_key = 'GregGuiCle'

env = os.getenv('ENV', 'dev')
print(env)
app.credentials = credentials = utils.import_app_credentials("config/config." + env + ".yml")
auth_flow = authorize_user.get_auth_flow(credentials)
url = authorize_user.authorization_code_grant_flow(auth_flow)

@app.route("/")
def login():
    return render_template('index.html')

@app.route("/api/uber/login")
def login_uber():
    return redirect(url)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('login'))

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

@app.route("/api/products")
def products():
    lat = request.args['lat']
    lng = request.args['lng']
    uber_session = get_uber_session(credentials)
    uber_client = UberRidesClient(uber_session, sandbox_mode=(env != 'prod'))
    response = uber_client.get_products(lat, lng)
    times = response.json.get('products')

    return jsonify(times)

@app.route("/api/pickuptimes")
def pickuptime():
    lat = request.args['lat']
    lng = request.args['lng']
    uber_session = get_uber_session(credentials)
    uber_client = UberRidesClient(uber_session, sandbox_mode=(env != 'prod'))
    response = uber_client.get_pickup_time_estimates(lat, lng)
    times = response.json.get('times')

    return jsonify(times)

@app.route("/api/prices")
def prices():
    start_lat = request.args['start_lat']
    start_lng = request.args['start_lng']
    end_lat = request.args['end_lat']
    end_lng = request.args['end_lng']
    uber_session = get_uber_session(credentials)
    uber_client = UberRidesClient(uber_session, sandbox_mode=(env != 'prod'))
    response = uber_client.get_price_estimates(
        start_latitude=start_lat,
        start_longitude=start_lng,
        end_latitude=end_lat,
        end_longitude=end_lng,
        seat_count=2
    )
    estimate = response.json.get('prices')
    return jsonify(estimate)

@app.route("/api/uber/activity")
def activity():
    uber_session = get_uber_session(credentials)
    uber_client = UberRidesClient(uber_session, sandbox_mode=(env != 'prod'))
    response = uber_client.get_user_activity()
    history = response.json

    return jsonify(history)


if __name__ == "__main__":
    app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)))
