import hashlib
import datetime

def sha512(string: str):
    return hashlib.sha512(string.encode()).hexdigest()

def strptime_gcp(string: str):
    fmt = r"%Y-%m-%dT%H:%M:%S.%f%z"
    return datetime.datetime.strptime(string, fmt)

def strftime_gcp(dt: datetime.datetime):
    fmt = r"%Y-%m-%dT%H:%M:%S.%f%z"
    return dt.strftime(fmt)