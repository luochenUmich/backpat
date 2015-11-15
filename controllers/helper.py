from flask import session, flash
import datetime

def is_active():
    if 'last_activity' not in session:
        return False
    inactive_time = datetime.datetime.now() - session['last_activity']
    if inactive_time >= datetime.timedelta(minutes=5):
        flash('Session has expired. Please sign in again')
        destroy_session()
        return False
    else:
        return True

def destroy_session():
    session.pop('username', None)
    session.pop('last_activity', None)


# You only need to use these two functions from outside
def is_logged_in():
    if 'username' in session and is_active():
        return True
    else:
        return False

def update_last_activity():
    session['last_activity'] = datetime.datetime.now()
