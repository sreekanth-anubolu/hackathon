import os
import slack
from settings import SLACK_TOKEN
client = slack.WebClient(token=SLACK_TOKEN)

MSG_TYPE_VIEW = "view"
MSG_TYPE_ALERT = "alert"

table_msg_template = {
    "type": "section",
    "fields": []
}

divider_template = {
    "type": "divider"
}

header_template = {
    "type": "section",
    "text": {
        "type": "plain_text",
        "text": "***CL Shutdown ALERT****.",
        "emoji": True
    }
}

SUPPORTED_MSG_TYPE = [MSG_TYPE_VIEW, MSG_TYPE_ALERT]

def get_table_heading(heading_string):
    field_dict = {}
    field_dict["type"] = "mrkdwn"
    field_dict["text"] = "*" + heading_string + "*"
    print("get_table_heading:{}".format(field_dict))
    return field_dict

def get_table_value(value_string):
    field_dict = {}
    field_dict["type"] = "plain_text"
    field_dict["text"] = value_string
    print("get_table_value:{}".format(field_dict))
    return field_dict

def build_table_view_dict(vm):
    ret_dict = {}
    ret_dict["Id"] = vm.get("server_id")
    ret_dict["Name"] = vm.get("server_name")
    if vm.get("server_status") == "ACTIVE":
        ret_dict["Status/remaining time"] = vm.get("server_status") + "/" + vm.get("remain_time")
    else:
        ret_dict["Status"] = vm.get("server_status")
    ret_dict["Server type"] = vm.get("server_type")
    return ret_dict
    
        

def create_table_msg_view(vm):
    table_dict = build_table_view_dict(vm)
    fields = []
    for keys,value in table_dict.items():
        fields.append(get_table_heading(keys))
        fields.append(get_table_value(value))

    return {"type": "section", "fields": fields}
    

def post_to_slack(channel_id, msg_type, vm_list):
    if msg_type not in SUPPORTED_MSG_TYPE:
        return "error"
    blocks_list = []
    if msg_type == MSG_TYPE_ALERT:
        blocks_list.append(header_template)
    for vm in vm_list:
        blocks_list.append(create_table_msg_view(vm))
        blocks_list.append(divider_template)
    
    print("channel_id:{}, blocks_list:{}".format(channel_id, blocks_list))
    client.chat_postMessage(
                channel=channel_id,
                blocks=blocks_list)

        
        

        






