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
		
	query = """select r.reportid, c.commentid, c.dateCreated, c.comment, p.summary, r.postid, r.reportText, r.reportedByUsername, c.username, CASE WHEN u.active = 1 THEN 'Active' ELSE 'Banned' END as reportedUserStatus, u.active as userActive, c.active as commentActive, p.active as postActive
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
		
		showDeleteButton = (report["commentActive"] == 1) and (report["postActive"] == 1) and active == "1"
		showBanButton = (report["userActive"] == 1) and active == "1"
		
		htmlToReturn += report_grid_row_html.format(str(report["comment"])
												,url_for('admin_user_profile.show_user_profile') + "?username=" + str(report["username"])
												, str(report["username"])
												, url_for('post_view.show_post') + "?postid=" + str(report["postid"])
												, report["summary"]
												, ("" if (report["dateCreated"] == None) else report["dateCreated"].strftime("%m/%d/%y %I:%M%p"))
												, report["reportText"]
												, url_for('admin_user_profile.show_user_profile') + "?username=" + str(report["reportedByUsername"])
												,  report["reportedByUsername"]
												, ('default' if showDeleteButton else 'none')
												, url_for('reportlist.delete') + "?reportid=" + str(report["reportid"]) + "&list=" + list_type_qs
												, ('default' if showBanButton else 'none')
												, ('|&nbsp;' if showDeleteButton else '')
												, url_for('reportlist.ban_user') + "?reportid=" + str(report["reportid"]) + "&username=" + str(report["username"]) + "&list=" + list_type_qs
												, ('default' if (showBanButton and showDeleteButton) else 'none')
												, url_for('reportlist.ban_user_and_delete') + "?reportid=" + str(report["reportid"]) + "&username=" + str(report["username"]) +"&list=" + list_type_qs
												, url_for('reportlist.hide_report') + "?reportid=" + str(report["reportid"]) + "&list=" + list_type_qs + "&username=" + str(report["username"])
												, ('Un-hide Report' if list_type_qs == 'inactive' else 'Hide Report') )
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
	change_report_active_state_func(reportid)
	
	return redirect(url_for('reportlist.show_reports') + "?list=" + list_type_qs)
	
@reportlist.route('/admin/reportlist/ban_user',methods=['GET'])
def ban_user():
	if not is_logged_in():
		return redirect(url_for('user.user_login'))
	if (getAdminLevel() < 2):
		flash('You need to be an administrator to access this page')
		return redirect(url_for('main.main_route'))
	list_type_qs = request.args.get('list')
	username = request.args.get('username')
	reportid = request.args.get('reportid')
	
	#Do shit here
	ban_user_func(username)
	change_report_active_state_func(reportid)
	
	return redirect(url_for('reportlist.show_reports') + "?list=" + list_type_qs)
	
@reportlist.route('/admin/reportlist/delete',methods=['GET'])
def delete():
	if not is_logged_in():
		return redirect(url_for('user.user_login'))
	if (getAdminLevel() < 2):
		flash('You need to be an administrator to access this page')
		return redirect(url_for('main.main_route'))
	list_type_qs = request.args.get('list')
	reportid = request.args.get('reportid')
	
	#Do shit here
	succesful = remove_related_item_func(reportid)
	if(succesful):
		change_report_active_state_func(reportid)
	
	return redirect(url_for('reportlist.show_reports') + "?list=" + list_type_qs)
	
@reportlist.route('/admin/reportlist/ban_user_and_delete',methods=['GET'])
def ban_user_and_delete():
	if not is_logged_in():
		return redirect(url_for('user.user_login'))
	if (getAdminLevel() < 2):
		flash('You need to be an administrator to access this page')
		return redirect(url_for('main.main_route'))
	list_type_qs = request.args.get('list')
	reportid = request.args.get('reportid')
	username = request.args.get('username')
	
	#Do shit here
	succesful = remove_related_item_func(reportid)
	if (succesful):
		ban_user_func(username)
		change_report_active_state_func(reportid)
	
	return redirect(url_for('reportlist.show_reports')  + "?list=" + list_type_qs)
	
def remove_related_item_func(reportid):
	conn = mysql.connection
	cursor = conn.cursor(MySQLdb.cursors.DictCursor)
	reportInfo = getReportInfo(reportid)
	commentid = 0
	postid = 0
	if (reportInfo):
		commentid = reportInfo["commentid"]
		postid = reportInfo["postid"]
	if (commentid == 0 and postid != 0):
		query = """update post set active = 0 where postid = %s"""
		cursor.execute(query, (postid,))
		result = cursor.fetchone()
		if (cursor.rowcount > 0):
			flash('Post removed')
		conn.commit()
		cursor.close()
		return True
	elif (commentid != 0): 
		query = """update comment set active = 0 where commentid = %s"""
		conn = mysql.connection
		cursor = conn.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute(query, (commentid,))
		result = cursor.fetchone()
		if (cursor.rowcount > 0):
			flash('Comment removed')
		conn.commit()
		cursor.close()
		return True
	cursor.close()
	flash("Failed to remove item")
	return False
	
def ban_user_func(username):
	query = """update user set active = 0 where username = %s"""
	conn = mysql.connection
	cursor = conn.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute(query, (username,))
	result = cursor.fetchone()
	if (cursor.rowcount > 0):
		flash('User ' + username + ' has been banned')
	conn.commit()
	cursor.close()
	return
	
def change_report_active_state_func(reportid):
	query = """update report set active = (CASE WHEN active = 0 THEN 1 ELSE 0 END) where reportid = %s"""
		
	conn = mysql.connection
	cursor = conn.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute(query, (reportid,))
	conn.commit()
	cursor.close()
	return
	
def getReportInfo(reportid):
	query = """select * from report where reportid = %s"""
		
	conn = mysql.connection
	cursor = conn.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute(query, (reportid,))
	result=cursor.fetchone()
	cursor.close()
	return result