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

admin_user_profile = Blueprint('admin_user_profile', __name__,template_folder='views')
    
@admin_user_profile.route('/admin/user_profile',methods=['GET'])
def show_user_profile():
	username = request.args.get('username')
	list_type_qs = request.args.get('list')
	
	query = """select u.email, CASE WHEN u.adminLevel > 2 THEN 'Admin' WHEN u.adminLevel > 1 THEN 'Moderator' ELSE 'Normal User' END as adminLevelText, CASE WHEN u.active then 'Active' else 'Inactive' end as status, u.created_at
				from user u
				where u.username = %s""";
	conn = mysql.connection
	cursor = conn.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute(query, (username,))
	user = cursor.fetchone()
	if not user: #if user does not exist, throw error message
		return "Error: User does not exist"
		
	list_html = ""
	_a_p = ""
	_a_c = ""
	_a_r = ""
	if (list_type_qs == "comments"):
		_a_c = "active"
		list_html = get_user_comments(username)
	elif (list_type_qs == "reports"):
		_a_r = "active"
		list_html = get_user_reports(username)
	else: #show posts
		_a_p = "active"
		list_html = get_user_posts(username)
	cursor.close()

	return render_template('admin_user_profile.html', username=username, email=user["email"], usertype=user["adminLevelText"],status=user["status"]
	,registered_on=user["created_at"].strftime("%m/%d/%y %I:%M%p") ,a_p=_a_p, a_c=_a_c, a_r=_a_r, list=list_html)
	
def get_user_posts(username):
	post_template_html = open('views/post_template.html', 'r').read()
	htmlToReturn = ""
	query = """select p.postid, summary, description, dateCreated, dateLastModified, nc.ct
				from post p
				left join (select COUNT(*) as ct, postid from comment where active = 1 group by postid) nc on nc.postid = p.postid
				where p.active = 1 and username = %s order by dateCreated desc, dateLastModified, summary"""
	conn = mysql.connection
	cursor = conn.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute(query, (username,))
	post = cursor.fetchone()
	while(post):
		_dateInfo = str(post["dateCreated"].strftime("%m/%d/%y %I:%M%p"))
		dateLastModified = post["dateLastModified"]
		if(dateLastModified and dateLastModified != post["dateCreated"]):
			_dateInfo += " (edited on " + str(dateLastModified.strftime("%m/%d/%y %I:%M%p")) + ")"
		htmlToReturn += post_template_html.format(url_for('post_view.show_post') + "?postid=" + str(post["postid"]), post["summary"],post["description"],_dateInfo,post["ct"] )
		#htmlToReturn += render_template('post_template.html', postid=post["postid"], title=post["summary"], description=post["description"],dateInfo=_dateInfo)
		post = cursor.fetchone()
	cursor.close()
	
	return htmlToReturn
	
def get_user_reports(username):
	htmlToReturn = ""
	
	return htmlToReturn
	
def get_user_comments(username):
	htmlToReturn = ""
	template_comment_row = open('views/comment_row_grid.html', 'r').read()
	query = """select c.commentid, c.dateCreated, c.comment, p.summary, c.postid
				from comment c
				left join post p on p.postid = c.postid
				where c.username = %s"""
	conn = mysql.connection
	cursor = conn.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute(query, (username,))
	comments = cursor.fetchall()
	cursor.close()
	for comment in comments:
		htmlToReturn += template_comment_row.format(str(comment["comment"]), url_for('post_view.show_post') + "?postid" + str(comment["postid"]), comment["summary"], comment["dateCreated"].strftime("%m/%d/%y %I:%M%p"))
	return htmlToReturn