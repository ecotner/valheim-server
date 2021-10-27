from genericpath import exists
import os
import time
import datetime as dt
import json
import requests

HTTP_PORT = 9000
DT_FMT = "%Y-%m-%d %H:%M:%S.%f"
PREV_FILE = "prev_status.json"
SHUTDOWN_THRESHOLD = 15 * 60  # in seconds

if os.path.exists("prev_status.json"):
    os.remove(PREV_FILE)

while True:
    time.sleep(10)
    # get server status update
    try:
        response = requests.get(f"http://localhost:{HTTP_PORT}/status.json")
    except requests.exceptions.ConnectionError as e:
        print(f"Connection error: {e}")
        continue
    # if errors out, wait again
    code = response.status_code
    if code != 200:
        print(f"Error: HTTP response {code}")
        continue
    err = response.json()["error"]
    if err is not None:
        print(f"Server error: <{err}>")
        continue
    # get json payload and overwrite timestamp
    cur_status = response.json()
    t2 = dt.datetime.utcnow()
    cur_status["last_status_update"] = t2.strftime(DT_FMT)
    # if there are no players online, look for status file
    if cur_status["player_count"] == 0:
        # if there is no status file, create one and wait again
        if not os.path.exists(PREV_FILE):
            with open(PREV_FILE, "w+") as fp:
                json.dump(cur_status, fp)
            continue
        # else check time since last time someone was online
        with open(PREV_FILE, "r") as fp:
            prev_status = json.load(fp)
        t1 = dt.datetime.strptime(prev_status["last_status_update"], DT_FMT)
        diff = (t2 - t1) / dt.timedelta(seconds=1)
        print(f"{diff} seconds since someone was last online")
        # if time exceeds threshold, shut down instance
        if diff > SHUTDOWN_THRESHOLD:
            print(f"Server idle for {diff} seconds; shutting down")
    # else if there are players online, erase lockfile (if it exists) and wait again
    elif os.path.exists(PREV_FILE):
        os.remove(PREV_FILE)
        continue
