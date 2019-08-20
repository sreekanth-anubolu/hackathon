from slack import WebClient, RTMClient
from settings import SLACK_TOKEN

COMMANDS = ["start", "stop", "extend", "list"]

@RTMClient.run_on(event="message")
def on_message(**payload):
    web_client = payload["web_client"]
    data = payload["data"]
    subtype = data.get("subtype", None)
    if not subtype:
        channel_id = data["channel"]

        user = data["user"]
        command = data.get("text", "").lower()
        message = f"Hi <@{user}>!\n Invalid Command!. Use 'list' command to know available commands"

        print(f"Message Received by user {user} with command {command}")
        if command in COMMANDS:

            if command == "list":
                message = """Here are the list of commmands to explore
                List - Lists your centralite instances
                Start - Starts your central lite instance, ex: Start <Instance ID>
                Stop - Stops your central lite instance, ex: Stop <Instance ID>
                Extend - Extends your central lite instance for 2 hours, ex: Extend <Instance ID>
                """

        web_client.chat_postMessage(
            channel=channel_id,
            text= message
        )
        print(f"Replied to by user {user}")


rtm_client = RTMClient(token=SLACK_TOKEN)

rtm_client.start()
