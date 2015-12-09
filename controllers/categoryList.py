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

categorylist = Blueprint('categorylist', __name__,template_folder='views')
	
@categorylist.route('/admin/categorylist',methods=['GET'])
def show_categories():
	if not is_logged_in():
		return redirect(url_for('user.user_login'))
	if (getAdminLevel() < 2):
		flash('You need to be an administrator to access this page')
		return redirect(url_for('main.main_route'))
	list_type_qs = request.args.get('list')
	categoryid = 0
	if ('categoryid' in request.args):
		categoryid = int(request.args.get('categoryid'))
		
	categoryName = ""
	if (categoryid != 0):
		categoryName = getCategoryName(categoryid)
	query = """select categoryid, categoryName from category where active = %s"""
				
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
	
	category_row_html = open('views/category_row.html', 'r').read()
	category = cursor.fetchone()
	htmlToReturn = ""
	while(category):
		if(htmlToReturn == ""):
			htmlToReturn = """<br/><div class="row table_header" style="font-weight:bold;font-size:large;border:none !important;">
								<div class="col-sm-2" style="border-right:none">
									Category ID
								</div>
								<div class="col-sm-10" style="border-left:none">
									Category Name
								</div>
							</div> """
		htmlToReturn += category_row_html.format(str(category["categoryid"])
			, category["categoryName"]
			, url_for('categorylist.show_categories') + "?categoryid=" + str(category["categoryid"]) + "&list=" + list_type_qs
			, url_for('categorylist.change_category_status') + "?categoryid=" + str(category["categoryid"]) + "&list=" + list_type_qs
			, 'Hide' if active == "1" else 'Show')
		category = cursor.fetchone()
	
	cursor.close()
	if (htmlToReturn == ""):
		htmlToReturn = "No categories match these criteria"
		
	return render_template('categoryList.html', list=htmlToReturn, a_a = _a_a, a_i = _a_i, categoryid=categoryid, button_text = ("Add New Category" if categoryid == 0 else "Edit Category #" + str(categoryid)), categoryName = categoryName)

@categorylist.route('/admin/categorylist/update_category',methods=['POST'])
def update_category():
	if not is_logged_in():
		return redirect(url_for('user.user_login'))
	if (getAdminLevel() < 2):
		flash('You need to be an administrator to access this page')
		return redirect(url_for('main.main_route'))
	if ('list' not in request.form):
		return redirect(url_for('categorylist.show_categories'))
	list_type_qs = request.form['list']
	if ('categoryid' not in request.form or '_categoryName' not in request.form):
		return redirect(url_for('categorylist.show_categories') + "?list=" + list_type_qs)
	categoryid = request.form['categoryid']
	categoryName = request.form['_categoryName']
	
	conn = mysql.connection
	cursor = conn.cursor(MySQLdb.cursors.DictCursor)
	if (int(categoryid) == 0):
		query = """insert into category(categoryName, createdByUsername) values(%s, %s)"""
		cursor.execute(query, (categoryName,session['username'],))
		flash("Added category")
	else:
		query = """update category set categoryName = %s where categoryid = %s"""
		cursor.execute(query, (categoryName,categoryid,))
		flash("Updated category")
	conn.commit()
	cursor.close()
	 
	return redirect(url_for('categorylist.show_categories') + "?list=" + list_type_qs)
	
@categorylist.route('/admin/categorylist/change_category_status',methods=['GET'])
def change_category_status():
	if not is_logged_in():
		return redirect(url_for('user.user_login'))
	if (getAdminLevel() < 2):
		flash('You need to be an administrator to access this page')
		return redirect(url_for('main.main_route'))
	list_type_qs = request.args.get('list')
	categoryid = request.args.get('categoryid')
	
	conn = mysql.connection
	cursor = conn.cursor(MySQLdb.cursors.DictCursor)
	query = """update category set active = (CASE WHEN active = 0 THEN 1 else 0 end) where categoryid = %s"""
	cursor.execute(query, (categoryid,))
	cursor.close()
	conn.commit()
	 
	return redirect(url_for('categorylist.show_categories') + "?list=" + list_type_qs)
	
def getCategoryName(categoryid):
	conn = mysql.connection
	cursor = conn.cursor(MySQLdb.cursors.DictCursor)
	query = """select categoryName from category where categoryid = %s"""
	cursor.execute(query, (categoryid,))
	categoryName = ""
	categoryNameRow = cursor.fetchone()
	if (categoryNameRow):
		categoryName = categoryNameRow["categoryName"]
	cursor.close()
	return categoryName