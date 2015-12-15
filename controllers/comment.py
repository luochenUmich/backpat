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
		flash (json.dumps({'error':'postid not specified'}))
		return redirect(redirect_url(request))
	postid = request.args.get('postid')
	conn = mysql.connection
	cursor = conn.cursor()
	try:
		_username = session['username'] #TD: Add in login function/check
		if ('comment' not in request.form):
			return json.dumps({'error':'comment text not specified'})
		if ('parentCommentID' not in request.form or not is_int(request.form['parentCommentID'])):
			return json.dumps({'error':'parentCommentID not specified'})
		_comment = sanitize(request.form['comment']) #text of the comment
		_parentCommentid = int(sanitize(request.form['parentCommentID'])) #Make 0 to be reply to post	
		# validate the received values
		#print("\n" + str(postid) + " " + _username + " " + _comment + " " + _parentCommentid + "\n")
		if postid and _username and _comment and _parentCommentid != None:
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
	
@comment.route('/comment/report',methods=['POST'])
def reportComment():
	if not is_logged_in():
		return render_template('user_login.html')
	if 'postid' not in request.args:
		return json.dumps({'error':'post not specified'})
	commentid = 0
	postid = request.args.get('postid')
	
	conn = mysql.connection
	cursor = conn.cursor()
	try:
		_username = session['username'] 
		if ('reportText' not in request.form ):
			flash (json.dumps({'error':'report notes not specified'}))
			return redirect(redirect_url(request))
			
		if ('commentid' not in request.form  or not is_int(request.form['commentid'])):
			flash (json.dumps({'error':'comment to report not specified'}))
			return redirect(redirect_url(request))
			
		_reportText = sanitize(request.form['reportText']) #text of the ban report
		commentid = int(sanitize(request.form['commentid'])) #Commentid 
		
		if postid and _username and _reportText:
			# All Good, let's call MySQL
			cursor.execute("""insert into report (postid, commentid, reportText, reportedByUsername) values (%s, %s, %s, %s)""", (postid, commentid, _reportText, _username))
			reportid = cursor.lastrowid
			
			if reportid is not 0:
				conn.commit()
				flash('Your report has been submitted successfully! A moderator will review it shortly.')
				return redirect(url_for('post_view.show_post') + "?postid=" + postid)
			else:
				flash('Report could not be created due to SQL error')
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