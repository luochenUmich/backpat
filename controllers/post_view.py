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
    
@post_view.route('/')
def show_post():
	if not is_logged_in():
		return render_template('user_login.html')
	postid = request.args.get('postid')
	conn = mysql.connect()
	cursor = conn.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute("""select top 1 username, summary, description. dateCreated, dateLastModified
                    from post p
                    where postid = %s""", (post_id))
	post = cursor.fetchone()
    
	opUsername = post["username"]
    #Get all the comments
	comment_html = generateCommentTree(0, post_id, opUsername)
	dateInfo = str(post["dateCreated"])
	#if (post["dateLastModified"] and post["dateCreated"] != post["dateLastModified"]):
	#    dateInfo += "Last Modified: " + str(post["dateLastModified"])
	#name = generateUniquename(opUsername, postid, opUsername)
	conn.close()
	cursor.close()
    
    #post_html = render_template('post_view_post_template.html', title=post["summary"], uniqname=name, dateCreatedInfo=dateInfo, numComments=post["numComments"], description=post["comments"])
    
	return render_template('post_view.html', title=post["summary"], dateCreatedInfo=dateInfo, description=post["comments"], comment_section=comment_html)
    
def generateUniquename(username, postid, opUsername): #make this work better in future
    name = "uniqueName" + str(username) + "-" + str(postid)
    if (username == opUsername):
        name += " (OP)"
    return name
    
def generateCommentTree(commentid, postid, opUsername): #Returns the html of the comment tree starting at commentid recursively. If commentid = 0, start with the post itself
	if (postid == 0):
		comment_template_html = open('../views/comment_template.html', 'r').read()
	htmlToReturn = ""
	query = """select commentid, username, dateCreated, comment, CASE WHEN parentCommentid = 0 THEN 1 ELSE 0 END [expanded] from comment where active = 1 and """ + ("COALESCE(parentCommentid, 0) = 0 and postid = %s" if commentid == 0 else "parentCommentid = %s")
	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.execute(query, (postid) if commentid == 0 else (commentid))
	comment = cursor.fetchall()
	while(comment):
		childrenHtml = generateCommentTree(comment["commentid"], postid, opUsername)
		htmlToReturn += comment_template_html % (comment["commentid"], str(comment["dateCreated"]), comment["comment"], childrenHtml)
		#htmlToReturn += render_template('comment_template.html', username=generateUniquename(comment["username"], postid, opUsername), dateCreated=str(comment["dateCreated"]), commentid=comment["commentid"], description=comment["comment"], comment_child_html=childrenHtml)
		comment = cursor.fetchone()
	conn.close()
	cursor.close()
	return htmlToReturn
