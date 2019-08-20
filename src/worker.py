import time
from timeloop import Timeloop
from datetime import timedelta

tl = Timeloop()

ALERT_REMAIN_TIME_MIN = 55
ALERT_REMAIN_TIME_MAX = 65

EXTEND_REMAIN_TIME = 60

# run a reminder for every 10 mins
@tl.job(interval=timedelta(seconds=6))
def cl_reminder_task():
    print("cl_reminder_task : ", time.ctime())

    time_stamp = time.time()

    print("do reminder task at : ", time_stamp)
    # go though all CL list of xyz table, and get remaining time for each CL.
    # If remaining time is in between "65 mins to 55 mins", raise a reminder

    try:
        servers = get_servers_list()

        for server_id, server_info in servers.items():

            try:
                print("server: ", server_id , " , and info: ", server_info)

                remain_time = server_info["remaining_time"]

                if remain_time is None:
                    print("remain_time is None, not a valid case server_info: {}".format(server_info))
                elif ALERT_REMAIN_TIME_MIN < remain_time < ALERT_REMAIN_TIME_MAX:
                    print("remain team {} is in range to raise a alert, and server_info: {} ".format(remain_time, server_info))
                    raise_alert(server_id, server_info)
                else:
                    print("no alert needed server_info: {}".format(remain_time))

            except Exception as e:
                print("Exception: {}".format(e))

    except Exception as e:
        print("cl_reminder_task: Exception: {}".format(e))


# extension task for every 10 mins
@tl.job(interval=timedelta(seconds=6000))
def cl_keepalive_task():

    try:
        print("cl_keepalive_task :", time.ctime())

    except Exception as e:
        print("cl_keepalive_task: Exception: {}".format(e))

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

                remain_time = server_info["remaining_time"]
                counter = server_info["counter"]
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
        "123": {"users_list": [], "remaining_time": 60, "keep_alive": False, "counter": 0},

        "223": {"users_list": [], "remaining_time": 66, "keep_alive": False, "counter": 0}
        }

    return servers


def raise_alert(server_id, server_info):
    print("********************************************************************************")
    print("raised alert for server_id: {} , server_info:{}".format(server_id, server_info))
    print("********************************************************************************")


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

