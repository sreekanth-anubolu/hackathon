from flask import Flask, render_template, request
from slack_utils import get_slackid_by_email
from users import Users

app = Flask(__name__, template_folder="frontend/templates/")


@app.route('/registration')
def register_view():
    return render_template("signup.html")

@app.route('/register',  methods=['POST'])
def register():
    cloudcop_username = request.form['cloudcop_username']
    cloudcop_password = request.form['cloudcop_password']
    slack_username = request.form['slack_username']
    user_obj = Users()
    if not user_obj.user_detail_exists(cloudcop_username):
        slack_uid = get_slackid_by_email(slack_username)
        user_obj.add_user_details(cloudcop_username, cloudcop_password, slack_username, slack_uid)
        return {"success" : "True"}
    return {"success": "False"}



if __name__ == '__main__':
    app.run()
