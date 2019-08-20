from copy import deepcopy
import time

CL_DETAILS = {}

server_details = { "users_list" : [], "end_time" : 0, "keep_alive" : False, "counter" : 0, "server_name": None, "server_type": "Central-Lite" }

def start_CL(server_id, server_name, end_time, user_id):
    details = deepcopy(server_details)
    details['users_list'].append(user_id)
    details['end_time'] = end_time
    details['server_name'] = server_name
    CL_DETAILS[server_id] = details


def stop_CL(server_id):
    CL_DETAILS.pop(server_id)


def extend_CL(server_id, server_name, user_id, end_time):
    details = deepcopy(server_details)
    details['users_list'].append(user_id)
    details['end_time'] = end_time
    details['server_name'] = server_name
    CL_DETAILS[server_id] = details


def keep_alive_CL(server_id, server_name, user_id,  num_of_hours, start_time=None, end_time=None):
    details = deepcopy(server_details)
    details['users_list'].append(user_id)
    details['end_time'] = end_time
    details['keep_alive'] = True
    details['server_name'] = server_name
    remaining_time = end_time - int(time.time())
    new_endtime = start_time + (num_of_hours * 3600 * 1000)
    diff_time = ((new_endtime - remaining_time * 60000)/3600000)
    counter = (diff_time/2) + 1
    details['counter'] = counter
    CL_DETAILS[server_id] = details


def get_CL_map():
    return CL_DETAILS


def update_CL_map(server_id, counter=None):
    if counter:
        CL_DETAILS[server_id]['counter'] = counter









