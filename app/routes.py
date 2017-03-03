import os
import services.uber_authorize_user as uber_authorize_user
import services.lyft_authorize_user as lyft_authorize_user

from flask import Flask, redirect, request, jsonify, session, url_for, render_template, g
from yaml import safe_dump
from uber_rides.session import OAuth2Credential, Session
from app import app, env
from middlewares.auth import get_vtc_session
from services.uber_credentials import auth_flow as uber_auth_flow, uber_url
from services.lyft_credentials import auth_flow as lyft_auth_flow, lyft_url
from db import db, User
from services.session_manager import create_session

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

@app.route("/api/lyft/login")
def login_lyft():
    if 'tokens' in session:
        return redirect(url_for('dashboard'))
        
    return redirect(lyft_url)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route("/api/uber/oauth", methods = ["GET"])
def uber_callback():
    oauth2credentials = uber_authorize_user.handle_callback(uber_auth_flow, request.url)
    existing_user = User.create_or_update('uber', oauth2credentials)
    create_session(existing_user);
   
    return redirect(url_for('dashboard'))
    
@app.route("/api/lyft/oauth", methods = ["GET"])
def lyft_callback():
    oauth2credentials = lyft_authorize_user.handle_callback(lyft_auth_flow, request.url)
    existing_user = User.create_or_update('lyft', oauth2credentials)
    create_session(existing_user);
    
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
    if 'tokens' not in session:
        return redirect(code=302, location=url_for('login'))
        
    lat = request.args['lat']
    lng = request.args['lng']
    response = g.uber_client.get_products(lat, lng)
    times = response.json.get('products')

    return jsonify(times)

@app.route("/api/pickuptimes")
def pickuptime():
    if 'tokens' not in session:
        return redirect(code=302, location=url_for('login'))
        
    lat = request.args['lat']
    lng = request.args['lng']
    response = g.uber_client.get_pickup_time_estimates(lat, lng)
    times = response.json.get('times')

    return jsonify(times)

@app.route("/api/prices")
def prices():
    if 'tokens' not in session:
        return redirect(code=302, location=url_for('login'))
        
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
    if 'tokens' not in session:
        return redirect(code=302, location=url_for('login'))
        
    response = g.uber_client.get_user_activity()
    history = response.json

    return jsonify(history)
