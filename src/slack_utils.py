
import requests
import json
from settings import SLACK_TOKEN

def get_slackid_by_email(email):
    api = f"https://slack.com/api/users.lookupByEmail?token={SLACK_TOKEN}&email={email}"
    resp = requests.get(api)
    if resp.status_code == 200:
        json_resp = json.loads(resp.content)
        return json_resp.get("user").get("id")