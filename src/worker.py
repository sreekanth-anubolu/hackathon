import time
from timeloop import Timeloop
from datetime import timedelta
from cl_details import get_CL_map, update_CL_map
from slack import WebClient
from settings import SLACK_TOKEN


from slack_msg_format import post_to_slack

tl = Timeloop()

ALERT_REMAIN_TIME_MIN = 5
ALERT_REMAIN_TIME_MAX = 65

EXTEND_REMAIN_TIME = 60


class BotChannel:
    channel_id = None

    @classmethod
    def get_bot_channel_id(cls, userID):
        if cls.channel_id:
            return cls.channel_id

        wc = WebClient(SLACK_TOKEN)
        res = wc.conversations_open(users=userID)
        cls.channel_id = res.get("channel").get("id")
        return cls.channel_id


# run a reminder for every 10 mins
@tl.job(interval=timedelta(seconds=200))
def cl_reminder_task():
    print("cl_reminder_task : ", time.ctime())

    time_stamp = time.time() * 1000

    print("do reminder task at : ", time_stamp)
    # go though all CL list of xyz table, and get remaining time for each CL.
    # If remaining time is in between "65 mins to 55 mins", raise a reminder

    try:
        servers = get_CL_map()

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
        servers = get_CL_map()

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
                    extend_server(server_id, server_info, counter, remain_time)
                else:
                    print("no alert needed server_info: {}".format(remain_time))

            except Exception as e:
                print("Exception: {}".format(e))

    except Exception as e:
        print("cl_keepalive_task: Exception: {}".format(e))


def get_servers_list():
    # MOCK FUNC
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

    for userid in set(users_list):
        channel_id = BotChannel.get_bot_channel_id(userid)
        post_to_slack(channel_id, "alert", vm_list)


def extend_server(server_id, server_info, counter, remain_time):
    print("********************************************************************************")
    print("extend server alert for server_id: {} , server_info:{}".format(server_id, server_info))
    print("********************************************************************************")

    vm_list = []
    vm1 = {}
    vm1["server_id"] = server_id
    vm1["server_name"] = server_info("server_name")
    vm1["server_status"] = "ON"
    vm1["remain_time"] = remain_time + " Mins"
    vm1["server_type"] = "Central-Lite"
    vm_list.append(vm1)

    # post_to_slack(channel_id, "keep_alias", vm_list)

    # reduce the counter
    update_CL_map(server_id, counter-1)


def start_worker(block=False):
    print("start worker")
    tl.start(block=block)
    print("stop worker")


if __name__ == "__main__":
    start_worker(True)

