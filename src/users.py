import psycopg2

from settings import CONN_STRING


class Users:
    def __init__(self):
        self.conn = psycopg2.connect(CONN_STRING)
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

 
