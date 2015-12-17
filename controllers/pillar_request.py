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
from datetime import date
import sys
import traceback

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
		print("\nPillar request type " + _pillarRequestTypeDropdownVal)
		sys.stdout.flush()
		if (_isTwoWay):
			isValidOneWay = checkPillarValidity(_username, _otherUsername)
			isValidOtherWay = checkPillarValidity(_otherUsername, _username)
			if (isValidOneWay == "" and isValidOtherWay == ""):
				cursor.execute("insert into pillar_request (username, supportUsername, reason, isTwoWay, requestedByUsername) values (%s, %s, %s, %s, %s)", (_username, _otherUsername, _reason, _isTwoWay, _username))
			else:
				flash(isValidOneWay + " " + isValidOtherWay)
				return redirect(redirect_url(request))
		elif (_pillarRequestTypeDropdownVal == "1"):
			isValidOtherWay = checkPillarValidity(_otherUsername, _username)
			if (isValidOtherWay == ""):
				cursor.execute("insert into pillar_request (username, supportUsername, reason, isTwoWay, requestedByUsername) values (%s, %s, %s, %s, %s)", (_otherUsername, _username, _reason, 0, _username))
			else:
				flash(isValidOtherWay)
				return redirect(redirect_url(request))
		else: 
			isValidOneWay = checkPillarValidity(_username, _otherUsername)
			if (isValidOneWay == ""):
				cursor.execute("insert into pillar_request (username, supportUsername, reason, isTwoWay, requestedByUsername) values (%s, %s, %s, %s, %s)", (_username, _otherUsername, _reason, 0, _username))
			else:
				flash(isValidOneWay)
				return redirect(redirect_url(request))
		cursorid = cursor.lastrowid

		if cursorid is not 0:
			conn.commit()
			flash("Pillar request sent")
			return redirect(redirect_url(request))
		else:
			flash("Pillar request could not be created, sorry!")
			return redirect(redirect_url(request))
	else:
		flash("Enter the required fields")
		return redirect(redirect_url(request))
		
def getUsernameFromCommentid(commentid):
	conn = mysql.connection
	cursor = conn.cursor(MySQLdb.cursors.DictCursor)
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
	cursor = conn.cursor(MySQLdb.cursors.DictCursor)
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
	cursor = conn.cursor(MySQLdb.cursors.DictCursor)
	query = """select username from user where email = %s"""
	cursor.execute(query, (email,))
	username = ""
	row = cursor.fetchone()
	if (row):
		username = row["username"]
	cursor.close()
	return username
	
def checkPillarValidity(username, supportUsername):
	print ("Checking pillar validity for " + username + " --> " + supportUsername)
	if (username == supportUsername):
		return "You cannot request yourself as a pillar"
	conn = mysql.connection
	cursor = conn.cursor()
	query = """select count(*) from pillar where supportUsername = %s and username = %s """
	cursor.execute(query, (supportUsername,username,))
	errorText = ""
	row = cursor.fetchone()
	if (row and is_int(row[0]) and int(row[0]) > 0):
		errorText += "This pillar relationship already exists"
	cursor.execute("select count(*) from pillar_request where supportUsername = %s and username = %s ", (supportUsername,username,))
	row = cursor.fetchone()
	if (row and is_int(row[0]) and int(row[0]) > 0):
		errorText += "There already exists a pending request for this pillar relationship"
	cursor.close()
	return errorText

@pillar_request.route('/pillar/remove',methods=['GET'])
def remove_pillar():
	if not is_logged_in():
		return render_template('user_login.html')

	_username = session['username'] 
	if ('otherUsername' not in request.args):
		flash('Specify another user username')
		return redirect(redirect_url(request))
	otherUsername = request.args['otherUsername']
	
	conn = mysql.connection
	cursor = conn.cursor()
	cursor.execute("""delete from pillar where (username = %s and supportUsername = %s) or (supportUsername = %s and username = %s)""", (_username, otherUsername, _username, otherUsername,))
	conn.commit()
	cursor.close()
	return ""
	
@pillar_request.route('/pillar/remove_request',methods=['GET'])
def remove_pillar_request():
	if not is_logged_in():
		return render_template('user_login.html')

	_username = session['username']
	if ('otherUsername' not in request.args):
		flash('Specify another user username')
		return redirect(redirect_url(request))
	
	conn = mysql.connection
	cursor = conn.cursor()
	cursor.execute("""delete from pillar_request where (username = %s and supportUsername = %s) or (supportUsername = %s and username = %s)""", (_username, otherUsername, _username, otherUsername,))
	conn.commit()
	cursor.close()
	return redirect(redirect_url(request))
	
@pillar_request.route('/pillar/accept',methods=['GET'])
def accept_pillar_request():
	if not is_logged_in():
		return render_template('user_login.html')

	_username = session['username']
	if ('otherUsername' not in request.args):
		flash('Specify another user username')
		return redirect(redirect_url(request))
	_otherUsername = request.args.get('otherUsername')
		
	pillarRequestInfo = getPillarRequestInfo(_username, _otherUsername)
	if (pillarRequestInfo):
		print("Pillar request info found")
		sys.stdout.flush()
		conn = mysql.connection
		cursor = conn.cursor()
		numToInsert = 0
		insertValues = None
		if(pillarRequestInfo["isTwoWay"]):
			print("\n\nTwo way: " + _username + "-" + _otherUsername + "\n\n")
			sys.stdout.flush()
			numToInsert = 2
			insertValues = (_username, _otherUsername, _otherUsername, _username)
		else:
			print("\n\nOne way\n\n")
			sys.stdout.flush()
			numToInsert = 1
			insertValues = (pillarRequestInfo["username"], pillarRequestInfo["supportUsername"])
		try:
			cursor.execute("""update pillar_request set dateAccepted = CURRENT_TIMESTAMP() where (username = %s or supportUsername = %s) and requestedByUsername = %s""", (_username, _username, _otherUsername)) 
			cursor.close()
			cursor = conn.cursor()
			cursor.execute("insert into pillar (username, supportUsername) values " + ("(%s,%s), (%s,%s);" if numToInsert > 1 else "(%s,%s);"), insertValues)
			conn.commit()
			flash('Pillar request accepted')
		except Exception as e:
			print("\n" + str(traceback.format_exception(*sys.exc_info())) + "\n")
			flash('Failed to accept pillar request')
		cursor.close()
	return redirect(redirect_url(request))
	
def getPillarRequestInfo(username, requestedByUsername):
	conn = mysql.connection
	cursor = conn.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute("""select * from pillar_request where ((supportUsername = %s or username = %s) and requestedByUsername = %s) limit 1""", (username, username, requestedByUsername))
	rVal = cursor.fetchone()
	cursor.close()
	return rVal