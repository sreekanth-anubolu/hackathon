import time
from timeloop import Timeloop
from datetime import timedelta

tl = Timeloop()

ALERT_REMAIN_TIME_MIN = 55
ALERT_REMAIN_TIME_MAX = 65

EXTEND_REMAIN_TIME = 60

# run a reminder for every 10 mins
@tl.job(interval=timedelta(seconds=600))
def cl_reminder_task():
    print("cl_reminder_task : ", time.ctime())

    time_stamp = time.time() * 1000

    print("do reminder task at : ", time_stamp)
    # go though all CL list of xyz table, and get remaining time for each CL.
    # If remaining time is in between "65 mins to 55 mins", raise a reminder

    try:
        servers = get_servers_list()

        for server_id, server_info in servers.items():

            try:
                print("server: ", server_id , " , and info: ", server_info)

                end_time = server_info["end_time"]
                remain_time = (end_time - time_stamp) / 60000 # divide by 60 sec*10000 ms to get minutes

                if remain_time < 1:
                    print("remain_time is negative, not a valid case server_info: {}".format(server_info))
                elif ALERT_REMAIN_TIME_MIN < remain_time < ALERT_REMAIN_TIME_MAX:
                    print("remain team {} is in range to raise a alert, and server_info: {} ".format(remain_time, server_info))
                    raise_alert(server_id, server_info, remain_time)
                else:
                    print("no alert needed server_info: {}".format(remain_time))

            except Exception as e:
                print("Exception: {}".format(e))

    except Exception as e:
        print("cl_reminder_task: Exception: {}".format(e))

# extension task for every 10 mins
@tl.job(interval=timedelta(seconds=6000))
def cl_keepalive_task():

    print("cl_keepalive_task :", time.ctime())

    time_stamp = time.time() * 1000

    # go though all CL list of xyz table, and get remaining time for each CL.
    # If remaining time is less than 30 mins and counter is non zero, extend the life.
    try:
        servers = get_servers_list()

        for server_id, server_info in servers.items():

            try:
                print("server: ", server_id, " , and info: ", server_info)

                if server_info["keep_alive"] is False or server_info["counter"] is 0:
                    print(" nothign to do, keep alive is false or counter is 0 for server_id:", server_id)
                    continue

                end_time = server_info["end_time"]
                counter = server_info["counter"]
                remain_time = (end_time - time_stamp) / 60000 # divide by 60 sec*10000 ms to get minutes

                if remain_time is None:
                    print("remain_time is None, not a valid case server_info: {}".format(server_info))
                elif remain_time < EXTEND_REMAIN_TIME:
                    print("remain team {} is in range to raise a alert, and server_info: {} ".format(remain_time, server_info))
                    extend_server(server_id, server_info)
                else:
                    print("no alert needed server_info: {}".format(remain_time))

            except Exception as e:
                print("Exception: {}".format(e))

    except Exception as e:
        print("cl_keepalive_task: Exception: {}".format(e))


def get_servers_list():

    servers = {
        "123": {"users_list": [], "end_time": None, "keep_alive": False, "counter": 0, "server_name": None,  "server_type": "Central-Lite"}
        }

    return servers


def raise_alert(server_id, server_info, remain_time):
    print("********************************************************************************")
    print("raised alert for server_id: {} , server_info:{}".format(server_id, server_info))
    print("********************************************************************************")
    users_list = server_info["users_list"]

    vm_list = []
    vm1 = {}
    vm1["server_id"] = server_id
    vm1["server_name"] = server_info("server_name")
    vm1["server_status"] = "ON"
    vm1["remain_time"] = remain_time + " Mins"
    vm1["server_type"] = "Central-Lite"
    vm_list.append(vm1)

    post_to_slack(users_list, "alert")
#  post_to_slack(channel_id, msg_type, vm_list):


def extend_server(server_id, server_info):
    print("********************************************************************************")
    print("extend server alert for server_id: {} , server_info:{}".format(server_id, server_info))
    print("********************************************************************************")

    #todo:
    # reduce the counter 


def start_worker(block=False):
    print("start worker")
    tl.start(block=block)
    print("stop worker")


if __name__ == "__main__":
    start_worker(True)

