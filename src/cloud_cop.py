#!/usr/bin/env python
import requests
import six.moves.urllib as urllib
import json


signin_url = 'https://cloudcop.arubathena.com/users/sign_in'
signin_post_url = 'https://cloudcop.arubathena.com/users/auth/ldap/callback'
servers_url = 'https://cloudcop.arubathena.com/server?per_page=20'
server_op_url = 'https://cloudcop.arubathena.com/server'
teams_url = 'https://cloudcop.arubathena.com/server/{}/teams'

from datetime import datetime
import time
def utc2local(utc_s):
    utc = datetime.strptime(utc_s, '%Y-%m-%dT%H:%M:%S.%fZ')
    epoch = time.mktime(utc.timetuple())
    offset = datetime.fromtimestamp (epoch) - datetime.utcfromtimestamp (epoch)
    return str(utc + offset)

class CloudCopClient:

    def __init__(self, username, password):
        self.sess = requests.Session()
        self.username = username
        self.password = password

    def __del__(self):
        self.sess.close()

    def _get_credentials(self):
        credential = {}
        credential['username'] = self.username
        credential['password'] = self.password
        return credential

    def login(self):
        credentials = self._get_credentials()

        try:
            r = self.sess.post(signin_post_url, data=credentials)
        except Exception as e:
            print(e)
            return

        if r.url != signin_url and r.cookies.get('XSRF-TOKEN'):
            token = urllib.parse.unquote(r.cookies.get('XSRF-TOKEN'))
            self.sess.headers.update({'X-XSRF-TOKEN': token})
            self.login_ok = True

    def list_servers(self):
        try:
            r = self.sess.get(servers_url)
        except Exception as e:
            print(e)
            return

        return json.loads(r.text)

    def _send_server_operation(self, params):
        try:
            r = self.sess.put(server_op_url, data=params)
            return r.ok
        except Exception as e:
            print(e)
            return False

    def start_server(self, id):
        params = {}
        params['id'] = id
        params['update_type'] = 'launch'
        return self._send_server_operation(params)

    def stop_server(self, id):
        params = {}
        params['id'] = id
        params['update_type'] = 'stop'
        return self._send_server_operation(params)

    def extend_server(self, id):
        params = {}
        params['id'] = id
        params['update_type'] = 'extend'
        return self._send_server_operation(params)
