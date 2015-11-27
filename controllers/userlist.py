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

userlist = Blueprint('userlist', __name__,template_folder='views')
    
@userlist.route('/admin/userlist',methods=['GET'])
def show_users():
	user_row_template_html = open('views/user_grid_row.html', 'r').read()
	htmlToReturn = ""
	query = """select u.username, u.email, CASE WHEN p.adminLevel > 2 THEN 'Admin' WHEN p.adminLevel > 1 THEN 'Moderator' ELSE 'Normal User' END as adminLevelText, CASE WHEN p.active then 'Active' else 'Inactive' end as activeStatus
				from user u
				left join permission p on u.username = p.username
				order by username""";
	conn = mysql.connection
	cursor = conn.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute(query)
	user_row = cursor.fetchone()
	while(user_row):
		htmlToReturn += post_template_html.format(url_for('admin.show_user_profile') + "?username=" + str(user_row["username"]), user_row["username"],user_row["email"],user_row["adminLevelText"],user_row["activeStatus"] )
		user_row = cursor.fetchone()
	cursor.close()
	return render_template('userlist.html', user_list=htmlToReturn)
	
