import os
import datetime
from flask import render_template, request
from backend.util import sha512, strftime_gcp
from backend.gcp import get_server_status, start_server, stop_server
from app import app

@app.get("/")
def home():
    return render_template("index.html")

@app.post("/get-info")
def get_info():
    if request.json["hash"] != sha512(os.environ["SECRET_PASSWORD"]):
        return {"status": "ok", "password_correct": False}
    payload = get_server_status()
    for k, v in payload.items():
        if isinstance(v, datetime.datetime):
            payload[k] = strftime_gcp(v)
    return {"status": "ok", "server_status": payload, "password_correct": True}

@app.post("/turn-on")
def turn_on():
    if request.json["hash"] != sha512(os.environ["SECRET_PASSWORD"]):
        return {"status": "ok", "password_correct": False}
    payload = start_server()
    for k, v in payload.items():
        if isinstance(v, datetime.datetime):
            payload[k] = strftime_gcp(v)
    return {"status": "ok", "response": payload, "password_correct": True}

@app.post("/turn-off")
def turn_off():
    if request.json["hash"] != sha512(os.environ["SECRET_PASSWORD"]):
        return {"status": "ok", "password_correct": False}
    payload = stop_server()
    for k, v in payload.items():
        if isinstance(v, datetime.datetime):
            payload[k] = strftime_gcp(v)
    return {"status": "ok", "response": payload, "password_correct": True}

@app.post("/confirm-password")
def confirm_password():
    payload = request.json
    if payload["hash"] == sha512(os.environ["SECRET_PASSWORD"]):
        return {"password_correct": True}
    else:
        return {"password_correct": False}