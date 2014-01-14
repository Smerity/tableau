import sys
sys.path.append("..")

import db.database

def get_logged_in(response):
    username = response.get_secure_cookie('userid')
    if username:
        username = username.decode()
        user = db.database.get_user(username)
        return user
    else:
        return None