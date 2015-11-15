from flask import session, flash
import datetime

def destroy_session():
    session.pop('username', None)
    session.pop('last_activity', None)


# You only need to use these two functions from outside
def is_logged_in():
    if 'username' in session and is_active():
        return True
    else:
        return False