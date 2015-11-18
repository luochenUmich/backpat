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
	global comment_template_html
	comment_template_html = open('views/comment_template.html', 'r').read()
	comment_html = generateCommentTree(0, postid, opUsername)
	#text_file = open("comment_output.html", "w+")
	#text_file.write(comment_html)
	#text_file.close()
	dateInfo = post["dateCreated"].strftime("%m/%d/%y %I:%M%p")
	#if (post["dateLastModified"] and post["dateCreated"] != post["dateLastModified"]):
	#    dateInfo += "Last Modified: " + str(post["dateLastModified"])
	#name = generateUniquename(opUsername, postid, opUsername)
    
    #post_html = render_template('post_view_post_template.html', title=post["summary"], uniqname=name, dateCreatedInfo=dateInfo, numComments=post["numComments"], description=post["comments"])
	return render_template('post_view.html', title=post["summary"], dateCreatedInfo=dateInfo, description=str(post["description"]),  postid=str(postid), comment_section=comment_html)
   
def generateUniquename(username, postid, opUsername): #make this work better in future
    name = "uniqueName" + str(username) + "-" + str(postid)
    if (username == opUsername):
        name += " (OP)"
    return name
    
def generateCommentTree(commentid, postid, opUsername): #Returns the html of the comment tree starting at commentid recursively. If commentid = 0, start with the post itself
	htmlToReturn = ""
	query = """select commentid, username, dateCreated, comment from comment where active = 1 and """ + ("COALESCE(parentCommentid, 0) = 0 and postid = %s" if commentid == 0 else "parentCommentid = %s")
	conn = mysql.connection
	cursor = conn.cursor(MySQLdb.cursors.DictCursor)
	id = postid if commentid == 0 else commentid
	cursor.execute(query, (str(id)))
	comments = cursor.fetchall()
	cursor.close()
	for comment in comments:
		childrenHtml = generateCommentTree(comment["commentid"], postid, opUsername)
		display = "default" if childrenHtml != "" else "none"
		htmlToReturn += comment_template_html.format(str(comment["commentid"]), str(comment["comment"]), str(comment["commentid"]), str(id), display,comment["dateCreated"].strftime("%m/%d/%y %I:%M%p"), childrenHtml)
		#htmlToReturn += render_template('comment_template.html', username=generateUniquename(comment["username"], postid, opUsername), dateCreated=str(comment["dateCreated"]), commentid=comment["commentid"], description=comment["comment"], comment_child_html=childrenHtml)
	return htmlToReturn
