from flask import *
from extensions import mysql
from helper import *
import MySQLdb
import MySQLdb.cursors
import sys

pillar_request = Blueprint('pillar_request', __name__,template_folder='views')

@pillar_request.route('/pillar/request',methods=['POST'])
def create():
	if not is_logged_in():
		return render_template('user_login.html')

	_username = session['username'] #TD: Add in login function/check
	_commentidOfOtherUser = 0
	_postidOfOtherUser = 0
	_emailOfOtherUser = 0
	_pillarRequestTypeDropdownVal = 0
	_reason = ""
	_otherUsername = ""
	if ('_postidOfOtherUser' in request.form):
		_commentidOfOtherUser = sanitize(request.form['_commentidOfOtherUser'])
		if (_commentidOfOtherUser):
			_otherUsername = getUsernameFromCommentid(_commentidOfOtherUser)
	if ('_postidOfOtherUser' in request.form):
		_postidOfOtherUser = sanitize(request.form['_postidOfOtherUser'])
		if (_postidOfOtherUser):
			_otherUsername = getUsernameFromPostid(_postidOfOtherUser)
	if ('_emailOfOtherUser' in request.form):
		_emailOfOtherUser = sanitize(request.form['_emailOfOtherUser'])
		if (_emailOfOtherUser):
			_otherUsername = getUsernameFromEmail(_emailOfOtherUser)
	if ('_reason' in request.form):
		_reason = sanitize(request.form['_reason'])
	if ('_pillarRequestTypeDropdownVal' in request.form):
		_pillarRequestTypeDropdownVal = sanitize(request.form['_pillarRequestTypeDropdownVal'])
		
	if (_otherUsername and _otherUsername != ""):
		conn = mysql.connection
		
		_isTwoWay = (_pillarRequestTypeDropdownVal == "2")
		cursor = conn.cursor()
		if (_isTwoWay or _pillarRequestTypeDropdownVal == "0"):
			isValidOneWay = checkPillarValidity(username, supportUsername)
			isValidOtherWay = checkPillarValidity(supportUsername, username)
			if (isValidOneWay == "" and isValidOtherWay == ""):
				cursor.execute("insert into pillar_request (username, supportUsername, reason, isTwoWay) values (%s, %s, %s, %s)", (_username, _supportUsername, _reason, _isTwoWay, _username))
			else:
				flash(isValidOneWay + " " + isValidOtherWay)
				return redirect(redirect_url())
		else: 
			isValidOneWay = checkPillarValidity(username, supportUsername)
			if (isValidOneWay == ""):
				cursor.execute("insert into pillar_request (username, supportUsername, reason, isTwoWay) values (%s, %s, %s, %s)", (_supportUsername, _username, _reason, 0, _username))
			else:
				flash(isValidOneWay)
				return redirect(redirect_url())
		cursorid = cursor.lastrowid

		if cursorid is not 0:
			conn.commit()
			flash("Pillar request sent")
			return redirect(redirect_url())
		else:
			flash("Pillar request could not be created, sorry!")
			return redirect(redirect_url())
	else:
		flash("Enter the required fields")
		return redirect(redirect_url())
		
def getUsernameFromCommentid(commentid):
	conn = mysql.connection
	cursor = conn.cursor()
	query = """select username from comment where commentid = %s"""
	cursor.execute(query, (commentid,))
	username = ""
	row = cursor.fetchone()
	if (row):
		username = row["username"]
	cursor.close()
	return username
	
def getUsernameFromPostid(postid):
	conn = mysql.connection
	cursor = conn.cursor()
	query = """select username from post where postid = %s"""
	cursor.execute(query, (postid,))
	username = ""
	row = cursor.fetchone()
	if (row):
		username = row["username"]
	cursor.close()
	return username
	
def getUsernameFromEmail(email):
	conn = mysql.connection
	cursor = conn.cursor()
	query = """select username from user where email = %s"""
	cursor.execute(query, (email,))
	username = ""
	row = cursor.fetchone()
	if (row):
		username = row["username"]
	cursor.close()
	return username
	
def checkPillarValidity(username, supportUsername):
	conn = mysql.connection
	cursor = conn.cursor()
	query = """select count(*) from pillar where supportUsername = %s and username = %s """
	cursor.execute(query, (username,supportUsername,))
	errorText = ""
	row = cursor.fetchone()
	if (row):
		errorText += "This pillar relationship already exists"
	cursor.execute("select count(*) from pillar_request where supportUsername = %s and username = %s ", (username,supportUsername,))
	row = cursor.fetchone()
	if (row):
		errorText += "There already exists a pending request for this pillar relationship"
	cursor.close()
	return username