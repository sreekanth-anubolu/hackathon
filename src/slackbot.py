from slack import WebClient, RTMClient
from settings import SLACK_TOKEN
from worker import start_worker

ALLOWED_COMMANDS = ["commands", "start", "stop", "extend", "list", "keepalive"]


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


@RTMClient.run_on(event="message")
def on_message(**payload):
    web_client = payload["web_client"]
    data = payload["data"]
    subtype = data.get("subtype", None)
    if not subtype:
        channel_id = data["channel"]

        user = data["user"]
        message = data.get("text", "").lower()
        commands = message.split(" ")
        r_message = f"Hi <@{user}>!\n Invalid Command!. Use 'list' command to know available commands"
        print(f"Message Received by user {user} with command {message}")
        cmd = commands[0]
        if cmd in ALLOWED_COMMANDS:
            if cmd == "commands":
                r_message = """Here are the list of commmands to explore
                List - Lists your centralite instances
                Start - Starts your central lite instance, ex: Start <Instance ID>
                Stop - Stops your central lite instance, ex: Stop <Instance ID>
                Extend - Extends your central lite instance for 2 hours, ex: Extend <Instance ID>
                Keepalive - Keeps the server alive for given time, Keepalive <Instance ID> 10 - keeps server on for 10 more Hours
                """

        web_client.chat_postMessage(
            channel=channel_id,
            text=r_message
        )
        print(f"Replied to by user {user}")


rtm_client = RTMClient(token=SLACK_TOKEN)


start_worker()
rtm_client.start()
