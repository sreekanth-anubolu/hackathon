from flask import Flask, render_template, request
from users import get_slackid_by_email, Users

app = Flask(__name__, template_folder="frontend/templates/")


@app.route('/registration')
def register_view():
    return render_template("signup.html")

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


