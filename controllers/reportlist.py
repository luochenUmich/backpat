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

reportlist = Blueprint('reportlist', __name__,template_folder='views')
	
@reportlist.route('/admin/reportlist',methods=['GET'])
def show_reports():
	if not is_logged_in():
		return redirect(url_for('user.user_login'))
	if (getAdminLevel() < 2):
		flash('You need to be an administrator to access this page')
		return redirect(url_for('main.main_route'))
	list_type_qs = request.args.get('list')
		
	query = """select r.reportid, c.commentid, c.dateCreated, c.comment, p.summary, r.postid, r.reportText, r.reportedByUsername, c.username, CASE WHEN u.active = 1 THEN 'Active' ELSE 'Banned' END as reportedUserStatus, u.active
				from report r
				left join post p on p.postid = r.postid
				left join comment c on c.commentid = r.commentid
				left join user u on c.username = u.username
				where r.active = %s"""
				
	list_html = ""
	_a_a = ""
	_a_i = ""
	active = "0"
	if (list_type_qs == "inactive"):
		_a_i = "active"
	else: #show posts
		_a_a = "active"
		list_type_qs = "posts"
		active = "1"
		
	conn = mysql.connection
	cursor = conn.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute(query, (active,))
	
	report_grid_row_html = open('views/report_grid_row.html', 'r').read()
	report = cursor.fetchone()
	htmlToReturn = ""
	while(report):
		if(htmlToReturn == ""):
			htmlToReturn = """<br/><div class="row table_header" style="font-weight:bold;font-size:large">
								<div class="col-sm-3">
									Reported Comment
								</div>
								<div class="col-sm-2">
									Related Post
								</div>
								<div class="col-sm-2">
									Date Reported
								</div>
								<div class="col-sm-2">
									Notes on Report
								</div>
								<div class="col-sm-1">
									Reporter
								</div>
								<div class="col-sm-2">
									&nbsp;
								</div>
							</div> """
		htmlToReturn += report_grid_row_html.format(str(report["comment"])
												,url_for('admin_user_profile.show_user_profile') + "?username=" + str(report["username"])
												, str(report["username"])
												, url_for('post_view.show_post') + "?postid=" + str(report["postid"])
												, report["summary"]
												, report["dateCreated"].strftime("%m/%d/%y %I:%M%p")
												, report["reportText"]
												, url_for('admin_user_profile.show_user_profile') + "?username=" + str(report["reportedByUsername"])
												,  report["reportedByUsername"]
												, url_for('reportlist.hide_report') + "?reportid=" + str(report["reportid"]) + "&list=" + list_type_qs + "&username=" + report["username"]
												, ('Un-hide' if list_type_qs == 'inactive' else 'Hide') 
												, ('none' if report['active'] == 0 else 'default')
												, url_for('reportlist.ban_user') + "?username=" + report["username"] + "&list=" + list_type_qs)
												#, ('Ban ' + report["username"] if report['active'] == 1 else report["username"] + ' banned'))
		report = cursor.fetchone()
	
	cursor.close()
	if (htmlToReturn == ""):
		htmlToReturn = "No current reports match the criteria"
		
	return render_template('reportlist.html', list=htmlToReturn, a_a = _a_a, a_i = _a_i)

@reportlist.route('/admin/reportlist/hide_report',methods=['GET'])
def hide_report():
	if not is_logged_in():
		return redirect(url_for('user.user_login'))
	if (getAdminLevel() < 2):
		flash('You need to be an administrator to access this page')
		return redirect(url_for('main.main_route'))
	list_type_qs = request.args.get('list')
	username = request.args.get('username')
	reportid = request.args.get('reportid')
	
	#Do shit here
	
	query = """update report set active = (CASE WHEN active = 0 THEN 1 ELSE 0 END) where reportid = %s"""
		
	conn = mysql.connection
	cursor = conn.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute(query, (reportid,))
	conn.commit()
	cursor.close()
	
	return redirect(url_for('reportlist.show_reports') + "?username=" + username + "&list=" + list_type_qs)
	
@reportlist.route('/admin/reportlist/ban_user',methods=['GET'])
def ban_user():
	if not is_logged_in():
		return redirect(url_for('user.user_login'))
	if (getAdminLevel() < 2):
		flash('You need to be an administrator to access this page')
		return redirect(url_for('main.main_route'))
	list_type_qs = request.args.get('list')
	username = request.args.get('username')
	
	#Do shit here
	query = """update user set active = 0 where username = %s"""
	conn = mysql.connection
	cursor = conn.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute(query, (username,))
	result = cursor.fetchone()
	if (cursor.rowcount > 0):
		flash('User ' + username + ' has had their status changed')
	conn.commit()
	cursor.close()
	
	return redirect(url_for('reportlist.show_reports') + "?username=" + username + "&list=" + list_type_qs)