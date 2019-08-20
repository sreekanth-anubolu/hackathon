from flask import Flask
from flask import request
from users import get_slackid_by_email, Users

app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello World!"


@app.route('/<name>')
def hello_name(name):
    return "Hello {}!".format(name)

@app.route('/register',  methods=['POST'])
def register():
    payload = request.get_json()
    print(payload)
    cloudcop_username = payload['cloudcop_username']
    cloudcop_password = payload['cloudcop_password']
    slack_username = payload['slack_username']
    user_obj = Users()
    if not user_obj.user_detail_exists(cloudcop_username):
        slack_uid = get_slackid_by_email(slack_username)
        user_obj.add_user_details(cloudcop_username, cloudcop_password, slack_username, slack_uid)
        return {"success" : "True"}
    return {"success": "False"}



if __name__ == '__main__':
    app.run()


