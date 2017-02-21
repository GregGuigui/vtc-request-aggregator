import os
import services.authorize_user as authorize_user

from flask import Flask, redirect, request, jsonify, session, url_for, render_template, g
from yaml import safe_dump
from uber_rides.session import OAuth2Credential, Session
from app import app, env
from middlewares.auth import get_uber_session
from services.uber_credentials import auth_flow, uber_url

app.debug = True
app.secret_key = 'GregGuiCle'

app.config.update(dict(
  PREFERRED_URL_SCHEME = 'http' if env == 'dev' else 'https'
))

@app.route("/")
def login():
    if 'tokens' in session:
        return redirect(url_for('dashboard'))
        
    return render_template('index.html')

@app.route("/api/uber/login")
def login_uber():
    if 'tokens' in session:
        return redirect(url_for('dashboard'))
        
    return redirect(uber_url)

@app.route("/logout")
def logout():
    session.clear()
    print(url_for('login'))
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
    if 'tokens' not in session:
        return redirect(code=302, location=url_for('login'))
        
    if 'profile' not in session:
        response = g.uber_client.get_user_profile()
        profile = response.json
        session['profile'] = profile
        
    return render_template('dashboard.html', profile=session['profile'])

@app.route("/api/products")
def products():
    lat = request.args['lat']
    lng = request.args['lng']
    response = g.uber_client.get_products(lat, lng)
    times = response.json.get('products')

    return jsonify(times)

@app.route("/api/pickuptimes")
def pickuptime():
    lat = request.args['lat']
    lng = request.args['lng']
    response = g.uber_client.get_pickup_time_estimates(lat, lng)
    times = response.json.get('times')

    return jsonify(times)

@app.route("/api/prices")
def prices():
    start_lat = request.args['start_lat']
    start_lng = request.args['start_lng']
    end_lat = request.args['end_lat']
    end_lng = request.args['end_lng']
    response = g.uber_client.get_price_estimates(
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
    response = g.uber_client.get_user_activity()
    history = response.json

    return jsonify(history)
