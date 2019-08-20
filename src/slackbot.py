from slack import RTMClient
from settings import SLACK_TOKEN
from worker import start_worker
from cloud_cop import CloudCopClient
from users import Users
from cl_details import calculate_remaining_time
from slack_msg_format import *
from datetime import datetime, timedelta
from cl_details import start_CL, stop_CL, extend_CL

ALLOWED_COMMANDS = ["commands", "start", "stop", "extend", "list", "keepalive"]

server_list_cache = {}


def format_time(server):
    time = calculate_remaining_time(server.get('shutdown')) / 3600000
    suffix = " Mins"
    if time > 1:
        suffix = " Hrs"
    else:
        time = time * 60
    return format(time, ".2f") + suffix

def get_serverlist_formatted(server_list):
    vm_list = []
    self_server_list = server_list.get('servers')
    for server in self_server_list:
        server_dict = {}
        server_dict["server_id"] = str(server.get('id'))
        server_dict['server_name'] = server.get('name')
        server_dict['server_status'] = server.get('state')
        server_dict['remain_time'] = format_time(server)
        server_dict['server_type'] = server.get('environment').get('resource_handler').get('name')
        vm_list.append(server_dict)
        server_list_cache[str(server.get('id'))] = server_dict

    shared_server_list = server_list.get('shared_servers')
    for server in shared_server_list:
        server_dict = {}
        server_dict["server_id"] = str(server.get('id'))
        server_dict['server_name'] = server.get('name')
        server_dict['server_status'] = server.get('state')
        server_dict['remain_time'] = format_time(server)
        server_dict['server_type'] = server.get('environment').get('resource_handler').get('name')
        vm_list.append(server_dict)
        server_list_cache[str(server.get('id'))] = server_dict

    return vm_list


def update_cache(event, cloud_cop_obj, server_id, user_id, end_time):
    server = server_list_cache[server_id]
    if not server:
        server_list = cloud_cop_obj.list_servers()
        get_serverlist_formatted(server_list)

    server = server_list_cache[server_id]

    if event == "start":
        start_CL(server["server_id"], server["server_name"], end_time, user_id)
    elif event == "extend":
        extend_CL(server["server_id"], server["server_name"], end_time, user_id)


@RTMClient.run_on(event="message")
def on_message(**payload):
    print("payload_received:{}".format(payload))
    web_client = payload["web_client"]
    data = payload["data"]
    subtype = data.get("subtype", None)
    if not subtype:
        channel_id = data["channel"]

        user = data["user"]
        message = data.get("text", "").lower()
        commands = message.split(" ")
        r_message = f"Hi <@{user}>!\n Invalid Command!. Use 'Commands' command to know available commands"
        print(f"Message Received by user {user} with command {message}")
        cmd = commands[0]
        if cmd in ALLOWED_COMMANDS:
            #get username password from slackid
            user_obj = Users()
            slack_id = user
            cc_user  =user_obj.get_ccop_details(slack_id)
            username=cc_user["ccop_uname"].split('@')[0]
            password=cc_user["ccop_password"]
            print("username:{}".format(username))
            cloud_cop_obj = CloudCopClient(username, password)
            send_reply_flag = True
            r_message = f"Hi <@{user}>!\n action completed successfully"
            if cmd == "commands":
                r_message = """Here are the list of commmands to explore
                List - Lists your centralite instances
                Start - Starts your central lite instance, ex: Start <Instance ID>
                Stop - Stops your central lite instance, ex: Stop <Instance ID>
                Extend - Extends your central lite instance for 2 hours, ex: Extend <Instance ID>
                Keepalive - Keeps the server alive for given time, Keepalive <Instance ID> 10 - keeps server on for 10 more Hours
                """
            elif cmd == "list":
                server_list = cloud_cop_obj.list_servers()
                print("server_list:{}",format(server_list))
                vm_list = get_serverlist_formatted(server_list)
                post_to_slack(channel_id, "view", vm_list)
                send_reply_flag = False
            elif cmd == "start":
                #read server_id from the paylaoad
                server_id = commands[1]
                start_time = datetime.utcnow()
                end_time = start_time + timedelta(minutes=10)
                cloud_cop_obj.start_server(server_id)
                update_cache("start", cloud_cop_obj, server_id, slack_id, end_time)

            elif cmd == "stop":
                #read server_id from the paylaoad
                server_id = commands[1]
                vm_list = cloud_cop_obj.stop_server(server_id)
                stop_CL(server_id)

            elif cmd == "extend":
                #read server_id from the paylaoad
                server_id = commands[1]
                start_time = datetime.utcnow()
                end_time = start_time + timedelta(minutes=10)
                cloud_cop_obj.extend_server(server_id)
                update_cache("extend", cloud_cop_obj, server_id, slack_id, end_time)

            elif cmd == "keepalive":
                #read server_id from the paylaoad
                server_id = commands[1]
                hours = commands[2]

        if send_reply_flag is True:
            web_client.chat_postMessage(channel=channel_id,text=r_message)

        print(f"Replied to by user {user}")


rtm_client = RTMClient(token=SLACK_TOKEN)


start_worker()
rtm_client.start()
