import psycopg2
import requests
import json

conn_string = "host='localhost' dbname='vinutha' user='postgres' password='' "

token = "xoxb-725845908228-725869486916-PWXa1YCWHR0lHmk6aXYMrc37"


class Users:
    def __init__(self):
        self.conn = psycopg2.connect(conn_string)
        self.cursor = self.conn.cursor()

    def user_detail_exists(self, ccop_name):
        self.cursor.execute("SELECT slack_uid from users where ccop_uname = %s;",(ccop_name,))
        record = self.cursor.fetchone() 
        if record:
           print(record)
           return True
        return False
        
    def add_user_details(self, ccop_name, ccop_pw, slack_uname, slack_uid):
        self.cursor.execute("INSERT INTO users(slack_uid, slack_uname, ccop_uname, ccop_password) VALUES (%s, %s, %s, %s);", (slack_uid, slack_uname, ccop_name, ccop_pw))
        self.conn.commit()
        count = self.cursor.rowcount
        print (count, "Record inserted successfully into users table")


def get_slackid_by_email(email):
    api = f"https://slack.com/api/users.lookupByEmail?token={token}&email={email}"
    resp = requests.get(api)
    if resp.status_code == 200:
        json_resp = json.loads(resp.content)
        return json_resp.get("user").get("id")
 
