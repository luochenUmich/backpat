from flask import session, flash
from bs4 import BeautifulSoup
import datetime
from extensions import mysql, mail
from flask_mail import Message
import string
import random
from itsdangerous import URLSafeSerializer
import threading
import hashlib
import config
import MySQLdb.cursors
from datetime import date
import sys

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

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
		
def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

VALID_TAGS = ['strong', 'em', 'p', 'ul', 'li', 'br']

#Returns the contents, sanitized of invalid html tags
def sanitize(value):

    soup = BeautifulSoup(value)

    for tag in soup.findAll(True):
        if tag.name not in VALID_TAGS:
            tag.extract()

    return soup.renderContents()
	
def redirect_url(request, default='index'):
    return request.args.get('next') or \
           request.referrer or \
           url_for(default)