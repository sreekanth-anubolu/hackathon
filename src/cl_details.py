from copy import deepcopy
import time
from datetime import datetime

CL_DETAILS = {}

server_details = {"users_list": [], "end_time": 0, "keep_alive": False, "counter": 0,
                  "server_name": None, "server_type": "Central-Lite"}

def start_CL(server_id, server_name, end_utc, user_id):
    end_utc = datetime.strptime(end_utc, '%Y-%m-%dT%H:%M:%S.%fZ')
    end_time = int(time.mktime(end_utc.timetuple()) * 1000) + 19800000
    details = deepcopy(server_details)
    details['users_list'].append(user_id)
    details['end_time'] = end_time
    details['server_name'] = server_name
    CL_DETAILS[server_id] = details


def stop_CL(server_id):
    CL_DETAILS.pop(server_id)


def extend_CL(server_id, server_name, user_id, end_utc):
    end_utc = datetime.strptime(end_utc, '%Y-%m-%dT%H:%M:%S.%fZ')
    end_time = int(time.mktime(end_utc.timetuple()) * 1000) + 19800000
    details = deepcopy(server_details)
    details['users_list'].append(user_id)
    details['end_time'] = end_time
    details['server_name'] = server_name
    CL_DETAILS[server_id] = details


def keep_alive_CL(server_id, server_name, user_id,  num_of_hours, end_utc):
    current_time = int(time.time()) * 1000
    end_utc = datetime.strptime(end_utc, '%Y-%m-%dT%H:%M:%S.%fZ')
    end_time = int(time.mktime(end_utc.timetuple()) * 1000) + 19800000
    details = deepcopy(server_details)
    details['users_list'].append(user_id)
    details['end_time'] = end_time
    details['keep_alive'] = True
    details['server_name'] = server_name
    print(current_time, end_time)
    diff_hours = (end_time - current_time)/3600000
    print(diff_hours)
    counter = (num_of_hours - diff_hours)/2 + 1
    details['counter'] = counter
    CL_DETAILS[server_id] = details


def get_CL_map():
    return CL_DETAILS


def update_CL_map(server_id, counter=None):
    if counter:
        CL_DETAILS[server_id]['counter'] = counter

def calculate_remaining_time(end_utc):
    current_time = int(time.time()) * 1000
    end_utc = datetime.strptime(end_utc, '%Y-%m-%dT%H:%M:%S.%fZ')
    end_time = int(time.mktime(end_utc.timetuple()) * 1000) + 19800000
    remaining_time = end_time - current_time
    print(remaining_time)
    return remaining_time






