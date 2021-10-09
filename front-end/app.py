import datetime
import os
from flask import Flask, render_template, request
from flask.wrappers import Response
from dotenv import load_dotenv
from backend.util import sha512, strftime_gcp
from backend.gcp import get_server_status, start_server, stop_server

load_dotenv()

app = Flask(__name__)

@app.get("/")
def home():
    return render_template("index.html")

@app.get("/get-info")
def get_info():
    payload = get_server_status()
    for k, v in payload.items():
        if isinstance(v, datetime.datetime):
            payload[k] = strftime_gcp(v)
    return {"status": "ok", "server_status": payload}

@app.get("/turn-on")
def turn_on():
    payload = start_server()
    for k, v in payload.items():
        if isinstance(v, datetime.datetime):
            payload[k] = strftime_gcp(v)
    return {"status": "ok", "response": payload}

@app.get("/turn-off")
def turn_off():
    payload = stop_server()
    for k, v in payload.items():
        if isinstance(v, datetime.datetime):
            payload[k] = strftime_gcp(v)
    return {"status": "ok", "response": payload}