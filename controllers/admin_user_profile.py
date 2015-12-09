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
import sys

admin_user_profile = Blueprint('admin_user_profile', __name__,template_folder='views')
	
@admin_user_profile.route('/admin/user_profile',methods=['GET'])
def show_user_profile():
	if not is_logged_in():
		return redirect(url_for('user.user_login'))
	if (getAdminLevel() < 2):
		flash('You need to be an administrator to access this page')
		return redirect(url_for('main.main_route'))
	username = request.args.get('username')
	list_type_qs = request.args.get('list')
	
	query = """select u.email, CASE WHEN u.adminLevel >= 2 THEN 'Administrator' WHEN u.adminLevel >= 1 THEN 'Moderator' ELSE 'Normal User' END as adminLevelText, CASE WHEN u.active then 'Active' else 'Inactive' end as status, u.created_at
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
		list_type_qs = "posts"
	cursor.close()

	return render_template('admin_user_profile.html', username=username, email=user["email"], usertype=user["adminLevelText"],status=user["status"]
	,registered_on=user["created_at"].strftime("%m/%d/%y %I:%M%p") ,a_p=_a_p, a_c=_a_c, a_r=_a_r, list=list_html, list_type=list_type_qs, ban_button_text=("Ban User" if str(user["status"]) == "Active" else "Unban User") )
	
@admin_user_profile.route('/admin/user_profile/make_user_admin',methods=['GET'])
def make_user_admin():
	if not is_logged_in():
		return redirect(url_for('user.user_login'))
	if (getAdminLevel() < 2):
		flash('You need to be an administrator to access this page')
		return redirect(url_for('main.main_route'))
	username = request.args.get('username')
	
	query = """update user set adminLevel = 2 where username = %s and adminLevel != 2"""
	conn = mysql.connection
	cursor = conn.cursor()
	cursor.execute(query,(username,))
	result = cursor.fetchone()
	if (cursor.rowcount > 0):
		flash('User ' + username + ' is now an administrator!')
	conn.commit()
	cursor.close()
	
	return show_user_profile()
	
@admin_user_profile.route('/admin/user_profile/make_user_mod',methods=['GET'])
def make_user_moderator():
	if not is_logged_in():
		return redirect(url_for('user.user_login'))
	if (getAdminLevel() < 2):
		flash('You need to be an administrator to access this page')
		return redirect(url_for('main.main_route'))
	username = request.args.get('username')
	
	query = """update user set adminLevel = 1 where username = %s and adminLevel != 1"""
	conn = mysql.connection
	cursor = conn.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute(query, (username,))
	result = cursor.fetchone()
	if (cursor.rowcount > 0):
		flash('User ' + username + ' is now a moderator!')
	conn.commit()
	cursor.close()
	
	return show_user_profile()
	
@admin_user_profile.route('/admin/user_profile/make_user_normal',methods=['GET'])
def make_user_normal():
	if not is_logged_in():
		return redirect(url_for('user.user_login'))
	if (getAdminLevel() < 2):
		flash('You need to be an administrator to access this page')
		return redirect(url_for('main.main_route'))
	username = request.args.get('username')
	
	query = """update user set adminLevel = 0 where username = %s and adminLevel != 0"""
	conn = mysql.connection
	cursor = conn.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute(query, (username,))
	result = cursor.fetchone()
	if (cursor.rowcount > 0):
		flash('User ' + username + ' "is now a normal user!')
	conn.commit()
	cursor.close()
	
	return show_user_profile()
	
@admin_user_profile.route('/admin/user_profile/change_ban_status',methods=['GET'])
def change_ban_status():
	if not is_logged_in():
		return redirect(url_for('user.user_login'))
	if (getAdminLevel() < 2):
		flash('You need to be an administrator to access this page')
		return redirect(url_for('main.main_route'))
	username = request.args.get('username')
	print('Changing status of ' + username + '\n')
	sys.stdout.flush()
	
	query = """update user set active = (CASE WHEN active = 0 THEN 1 ELSE 0 END) where username = %s"""
	conn = mysql.connection
	cursor = conn.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute(query, (username,))
	result = cursor.fetchone()
	if (cursor.rowcount > 0):
		flash('User ' + username + ' has had their status changed')
	conn.commit()
	cursor.close()
	
	return redirect(url_for('admin_user_profile.show_user_profile') + "?username=" + username);
	
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
	
	query = """select r.reportid, c.commentid, c.dateCreated, c.comment, p.summary, r.postid, r.reportText, CASE WHEN r.active = 1 THEN 'Unresolved' ELSE 'Resolved' END as reportStatus
				from report r
				left join post p on p.postid = r.postid
				left join comment c on c.commentid = r.commentid
				left join user u on c.username = u.username
				where c.username = %s"""
		
	conn = mysql.connection
	cursor = conn.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute(query, (username,))
	
	report_grid_row_html = open('views/report_grid_row_user_profile.html', 'r').read()
	report = cursor.fetchone()
	while(report):
		if(htmlToReturn == ""):
			htmlToReturn = """<br/><div class="row table_header" style="font-weight:bold;font-size:large">
								<div class="col-sm-4">
									Your Comment
								</div>
								<div class="col-sm-2">
									Related Post
								</div>
								<div class="col-sm-2">
									Date Reported
								</div>
								<div class="col-sm-2">
									Report Notes
								</div>
								<div class="col-sm-2">
									Status
								</div>
							</div> """
		htmlToReturn += report_grid_row_html.format(str(report["comment"])
												, url_for('post_view.show_post') + "?postid" + str(report["postid"])
												, report["summary"]
												, report["dateCreated"].strftime("%m/%d/%y %I:%M%p")
												, report["reportText"]
												, report["reportStatus"])
		
		report = cursor.fetchone()
	
	cursor.close()
	if (htmlToReturn == ""):
		htmlToReturn = "No current reports match the criteria"
	
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
		htmlToReturn += template_comment_row.format(str(comment["comment"]), url_for('post_view.show_post') + "?postid=" + str(comment["postid"]), comment["summary"], comment["dateCreated"].strftime("%m/%d/%y %I:%M%p"))
	return htmlToReturn