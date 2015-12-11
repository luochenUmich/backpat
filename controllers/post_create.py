from flask import *
from extensions import mysql
from helper import *
import MySQLdb
import MySQLdb.cursors
import sys

post_create = Blueprint('post_create', __name__,template_folder='views')

@post_create.route('/post/create',methods=['GET'])
def post_route():
	if not is_logged_in():
		return render_template('user_login.html')	 
	
	return render_template('post_create.html', categories=categories)

@post_create.route('/post/create',methods=['POST'])
def create():
	if not is_logged_in():
		return render_template('user_login.html')

	_username = session['username'] #TD: Add in login function/check
	_summary = sanitize(request.form['_summary'])
	_description = sanitize(request.form['_description'])
	_categoryid = 0
	if ('_categoryid' in request.form):
		_categoryid = request.form['_categoryid']
		print("Category id in form\n");
		sys.stdout.flush()

	# validate the received values
	if _username and _summary and _description:

		# All Good, let's call MySQL
		conn = mysql.connection
		cursor = conn.cursor()
		cursor.execute("insert into post (username, summary, description, categoryid) values (%s, %s, %s, %s)", (_username, _summary, _description, _categoryid))

		cursorid = cursor.lastrowid

		if cursorid is not 0:
			conn.commit()
			return redirect(url_for('post_view.show_post', postid=cursorid))
		else:
			return json.dumps({'error':"Post could not be created: "})
	else:
		return json.dumps({'html':'<span>Enter the required fields</span>'})
