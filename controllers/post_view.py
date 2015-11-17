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

post_view = Blueprint('post_view', __name__)
comment_template_html = ""
    
@post_view.route('/post/view')
def show_post():
	if not is_logged_in():
		return render_template('user_login.html')
	if 'postid' not in request.args:
		return json.dumps({'error':'postid not specified'})
	postid = request.args.get('postid')
	conn = mysql.connection
	cursor = conn.cursor(MySQLdb.cursors.DictCursor)
	print("Reading database info for post: " + postid)
	cursor.execute("""select username, summary, description, dateCreated, dateLastModified
                    from post p
                    where postid = %s
					limit 1""", (postid))
	post = cursor.fetchone()
	cursor.close()
	if not post:
		return json.dumps({'error':'postid not valid'})
	
	opUsername = post["username"]
    #Get all the comments
	comment_html = generateCommentTree(0, postid, opUsername)
	dateInfo = str(post["dateCreated"])
	#if (post["dateLastModified"] and post["dateCreated"] != post["dateLastModified"]):
	#    dateInfo += "Last Modified: " + str(post["dateLastModified"])
	#name = generateUniquename(opUsername, postid, opUsername)
    
    #post_html = render_template('post_view_post_template.html', title=post["summary"], uniqname=name, dateCreatedInfo=dateInfo, numComments=post["numComments"], description=post["comments"])
    
	return render_template('post_view.html', title=post["summary"], dateCreatedInfo=dateInfo, description=post["description"], comment_section=comment_html)
    
def generateUniquename(username, postid, opUsername): #make this work better in future
    name = "uniqueName" + str(username) + "-" + str(postid)
    if (username == opUsername):
        name += " (OP)"
    return name
    
def generateCommentTree(commentid, postid, opUsername): #Returns the html of the comment tree starting at commentid recursively. If commentid = 0, start with the post itself
	if (postid == 0):
		comment_template_html = open('../views/comment_template.html', 'r').read()
	htmlToReturn = ""
	query = """select commentid, username, dateCreated, comment from comment where active = 1 and """ + ("COALESCE(parentCommentid, 0) = 0 and postid = %s" if commentid == 0 else "parentCommentid = %s")
	print(query)
	conn = mysql.connection
	cursor = conn.cursor()
	id = postid if commentid == 0 else commentid
	print(id)
	cursor.execute(query, (id))
	comments = cursor.fetchall()
	cursor.close()
	for comment in comments:
		childrenHtml = generateCommentTree(comment["commentid"], postid, opUsername)
		htmlToReturn += comment_template_html % (comment["commentid"], str(comment["dateCreated"]), comment["comment"], childrenHtml)
		#htmlToReturn += render_template('comment_template.html', username=generateUniquename(comment["username"], postid, opUsername), dateCreated=str(comment["dateCreated"]), commentid=comment["commentid"], description=comment["comment"], comment_child_html=childrenHtml)
	return htmlToReturn
