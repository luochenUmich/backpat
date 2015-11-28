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

user = Blueprint('user', __name__, template_folder='views')

@user.route('/user/login', methods=['GET', 'POST'])
def user_login():
	if request.method == 'GET' and 'username' not in session:
		return render_template('user_login.html')
	elif request.method == 'GET' and 'username' in session:
		return redirect(url_for('main.main_route'))
	else:
		# Check if user exists and if password is correct
		conn = mysql.connection
		cur = conn.cursor(MySQLdb.cursors.DictCursor)
		cur.execute("SELECT * FROM user WHERE USERNAME='%s'" % request.form['username'])
		user = cur.fetchone()
		if user is None:
			flash('Username does not exist!')
			return render_template('user_login.html')

		# Forget password or password is not correct
		if hashlib.md5(request.form['password']).hexdigest() != user['password']:
			flash('Wrong password! Please try again')
			return render_template('user_login.html', prev_url=request.args.get('url'))

		# Set up the session
		session['username'] = request.form['username']
		session['adminLevel'] = user['adminLevel']
		return redirect(url_for('main.main_route'))

@user.route('/logout', methods=['GET'])
def user_logout():
	destroy_session()
	return redirect(url_for('main.main_route'))

@user.route('/user', methods=['GET','POST'])
def user_register():
	if request.method == 'GET':
		# return the register page
		return render_template('user_register.html')
	else:
		# check if two passwords match
		if (request.form['password'] != request.form['password_confirm']):
			flash("Password must match!")
			return render_template('user_register.html')

		# check if username already exists
		conn = mysql.connection
		cur = conn.cursor(MySQLdb.cursors.DictCursor)
		cur.execute("SELECT * FROM user WHERE USERNAME='%s'" % request.form['username'])
		res = cur.fetchall()
		if (len(res) >= 1):
			flash('Username already exists!')
			return render_template('user_register.html')

		# insert the user to database
		password_hash = hashlib.md5(request.form['password']).hexdigest()
		cur.execute("INSERT INTO user (USERNAME, PASSWORD, EMAIL, ADMINLEVEL) "
					"VALUES ('%s', '%s', '%s', 0)" % (request.form['username'],
					password_hash, request.form['email']))
		conn.commit()

		session['username'] = request.form['username']
		return redirect(url_for('main.main_route'))

@user.route('/profile', methods=['GET'])
def user_profile():
	if 'username' not in session:
		return render_template('user_login.html')
	else:
		# Check if user exists and if password is correct
		conn = mysql.connection
		cur = conn.cursor(MySQLdb.cursors.DictCursor)
		cur.execute("SELECT * FROM POST WHERE USERNAME='%s'" % session['username'])
		posts = cur.fetchall()
		return render_template('user_profile.html', posts=posts)

@user.route('/user/delete', methods=['GET'])
def user_delete():
	if not is_logged_in():
		return redirect(url_for('user.user_login'))

	conn = mysql.connection
	cur = conn.cursor(MySQLdb.cursors.DictCursor)

	# delete user
	cur.execute("DELETE FROM user WHERE USERNAME='%s'" % session['username'])
	conn.commit()

	# destroy session
	destroy_session()
	return redirect(url_for('main.main_route'))

