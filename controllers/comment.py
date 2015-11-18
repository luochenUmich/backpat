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
	if 'postid' not in request.args:
		return json.dumps({'error':'postid not specified'})
	postid = request.args.get('postid')
	conn = mysql.connection
	cursor = conn.cursor()
	try:
		_username = session['username'] #TD: Add in login function/check
		if ('comment' not in request.form):
			return json.dumps({'error':'comment text not specified'})
		if ('parentCommentID' not in request.form):
			return json.dumps({'error':'parentCommentID not specified'})
		_comment = request.form['comment'] #text of the comment
		_parentCommentid = request.form['parentCommentID'] #Make 0 to be reply to post	
		# validate the received values
		#print("\n" + str(postid) + " " + _username + " " + _comment + " " + _parentCommentid + "\n")
		if postid and _username and _comment and _parentCommentid:
			# All Good, let's call MySQL
			cursor.execute("""insert into comment (postid, parentCommentid, username, comment) values (%s, %s, %s, %s)""", (postid, _parentCommentid, _username, _comment))
			commentid = cursor.lastrowid
			
			if commentid is not 0:
				conn.commit()
				return redirect(url_for('post_view.show_post') + "?postid=" + postid)
			else:
				flash('Comment could not be created due to SQL error')
				return redirect(url_for('post_view.show_post') + "?postid=" + postid)
		else:
			flash('Enter the required fields')
			return redirect(url_for('post_view.show_post') + "?postid=" + postid)
			
	except Exception as e:
		flash('Internal server error: ' + str(e))
		return redirect(url_for('post_view.show_post') + "?postid=" + postid)
	finally:
		if (cursor):
			cursor.close()
	