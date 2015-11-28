from flask import session, flash
import datetime

def destroy_session():
	session.pop('username', None)
	session.pop('last_activity', None)
	session.pop('adminLevel',None)


# You only need to use these two functions from outside
def is_logged_in():
	if 'username' in session:
		return True
	else:
		return False
		
def getAdminLevel():
	if 'adminLevel' in session:
		return int(session.get('adminLevel'))
	else:
		return 0
