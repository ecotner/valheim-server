""" Tools for interacting with the GCP HTTP API
"""
import os
from google.auth import load_credentials_from_file
from google.cloud.compute import InstancesClient, Instance
from dotenv import load_dotenv
from backend.util import strptime_gcp

load_dotenv()

key_file = os.environ["GCP_KEY_FILE"]
credentials, project = load_credentials_from_file(key_file)
client = InstancesClient(credentials=credentials)
request_kwargs = {
    "project": project,
    "zone": os.environ["GCP_ZONE"],
    "instance": os.environ["GCP_INSTANCE_NAME"],
}

def get_server_status():
    """ Queries the server to get status payload, then filters down
    to important information.
    
    See https://cloud.google.com/compute/docs/reference/rest/v1/instances/get
    for info about the payload returned.
    """
    response = client.get(**request_kwargs)
    payload = {}
    payload["status"] = response.status.name
    # payload["machine_type"] = response.machine_type
    payload["last_start"] = strptime_gcp(response.last_start_timestamp)
    payload["last_stop"] = strptime_gcp(response.last_stop_timestamp)
    net_int = response.network_interfaces
    payload["internal_ip"] = net_int[0].network_i_p
    payload["external_ip"] = net_int[0].access_configs[0].nat_i_p
    return payload

def start_server():
    """ Starts the valheim server

    See https://cloud.google.com/compute/docs/reference/rest/v1/instances/start
    for info about the returned payload
    """
    response = client.start(**request_kwargs)
    payload = {}
    payload["status"] = response.status.name
    payload["status_message"] = response.status_message
    payload["start_time"] = strptime_gcp(response.start_time)
    # payload["end_time"] = strptime_gcp(response.end_time)
    # these aren't JSON-serializable:
    # payload["error"] = response.error
    # payload["warnings"] = response.warnings
    payload["description"] = response.description
    payload["kind"] = response.kind
    return payload

def stop_server():
    """ Stops the valheim server

    See https://cloud.google.com/compute/docs/reference/rest/v1/instances/stop
    for info about the returned payload
    """
    response = client.stop(**request_kwargs)
    payload = {}
    payload["status"] = response.status.name
    payload["status_message"] = response.status_message
    payload["start_time"] = strptime_gcp(response.start_time)
    # payload["end_time"] = strptime_gcp(response.end_time)
    # these aren't JSON-serializable:
    # payload["error"] = response.error
    # payload["warnings"] = response.warnings
    payload["description"] = response.description
    payload["kind"] = response.kind
    return payload