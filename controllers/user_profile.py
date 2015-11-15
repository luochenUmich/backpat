from flask import *
from helper import *
from extensions import mysql, mail
from flask_mail import Message
import string
import random
from itsdangerous import URLSafeSerializer
import threading
import hashlib
import config
import MySQLdb.cursors

user = Blueprint('user_profile', __name__, template_folder='views')

@user.route('/user_porfile', methods=['GET'])
def user_login():
    if 'username' not in session:
        return render_template('user_login.html')
    else:
        # Check if user exists and if password is correct
        conn = mysql.connection
        cur = conn.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM POST WHERE USERNAME='%s'" % session['username'])
        posts = cur.fetchall()
        return render_template('user_profile.html', posts=posts)
        