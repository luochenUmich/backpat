from flask import *
from extensions import mysql
from helper import *
import MySQLdb
import MySQLdb.cursors

comment = Blueprint('comment', __name__)

@comment.route('/comment',methods=['POST'])
def makeComment():
	if not is_logged_in():
		return render_template('user_login.html')
	postid = request.args.get('postid')
	try:
		_username = session['username'] #TD: Add in login function/check
		_comment = request.form['_comment'] #text of the comment
		_parentCommentid = request.form['_parentCommentid'] #Make 0 to be reply to post
		# validate the received values
		if postid and _username and _comment and _parentCommentid:
			# All Good, let's call MySQL
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute("""insert into comment (postid, parentCommentid, username, comment) values (%s, %s, %s, %s)""", (_postid, _parentCommentid, _username, _comment))
			commentid = cursor.lastrowid
			
			if commentid is not 0:
				conn.commit()
				return show_post()
			else:
				flash('Comment could not be created due to SQL error')
				return show_post()
		else:
			flash('Enter the required fields')
			return show_post()
			
	except Exception as e:
		flash('Internal server error: ' + str(e))
	finally:
		cursor.close() 
		conn.close()