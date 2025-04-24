from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from datetime import datetime
import math
from .services.token_manager import get_access_token
from .services.arduino_cloud import get_variable_value, set_variable_value
from .models import db
from flask_login import login_required, current_user 

views = Blueprint('views', __name__)

THING_ID = "3284f568-841e-4717-9604-cfcdb38f1e39"

@views.route('/')
def home():
    return render_template("home.html", user=current_user)

@views.route('/dashboard')
@login_required
def dashboard():
    token = get_access_token()

    temperature = get_variable_value(token, THING_ID, "a709e627-32a5-47b8-b757-ad74872a0e93")
    emergency_button = get_variable_value(token, THING_ID, "b1419324-d9bc-43f7-ab95-6d963aa4f55d")
    location = get_variable_value(token, THING_ID, "a5813ce3-46c0-4e6a-93d1-bc9ecc7f571f")

    lat = str(location.get('lat', 0)).strip() if location else "0"
    lon = str(location.get('lon', 0)).strip() if location else "0"

    return render_template(
        "dashboard.html",
        temperature=round(float(temperature), 2),
        lat=lat,
        lon=lon,
        emergency_button=bool(emergency_button)
    )

@views.route("/trigger-emergency", methods=["POST"])
def trigger_emergency():
    token = get_access_token()
    emergency_property_id = "b1419324-d9bc-43f7-ab95-6d963aa4f55d"

    if not token:
        print("⚠️ Không lấy được access token")
        return redirect(url_for("views.dashboard"))

    success = set_variable_value(token, THING_ID, emergency_property_id, 1)

    print("✅ Đã gửi tín hiệu khẩn cấp!" if success else "❌ Gửi thất bại!")
    return redirect(url_for("views.dashboard"))

@views.route('/api/status')
def get_status():
    token = get_access_token()
    temperature = get_variable_value(token, THING_ID, "a709e627-32a5-47b8-b757-ad74872a0e93")
    emergency_button = get_variable_value(token, THING_ID, "b1419324-d9bc-43f7-ab95-6d963aa4f55d")
    location = get_variable_value(token, THING_ID, "a5813ce3-46c0-4e6a-93d1-bc9ecc7f571f")

    return jsonify({
        "temperature": round(float(temperature), 2),
        "emergency_button": bool(emergency_button),
        "lat": location.get("lat", 0) if location else 0,
        "lon": location.get("lon", 0) if location else 0
    })

@views.route('/trackWorkout')
def trackWorkout():
    token = get_access_token()

    temperature = get_variable_value(token, THING_ID, "a709e627-32a5-47b8-b757-ad74872a0e93")
    emergency_button = get_variable_value(token, THING_ID, "b1419324-d9bc-43f7-ab95-6d963aa4f55d")
    location = get_variable_value(token, THING_ID, "a5813ce3-46c0-4e6a-93d1-bc9ecc7f571f")

    lat = str(location.get('lat', 0)).strip() if location else "0"
    lon = str(location.get('lon', 0)).strip() if location else "0"

    return render_template("trackWorkout2.html",
                           temperature=round(float(temperature), 2),
                           lat=lat,
                           lon=lon,    
                           emergency_button=bool(emergency_button),
                           location=location
                         )
