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
	cursor.execute("""select p.username, p.summary, p.description, p.dateCreated, p.dateLastModified, c.categoryName, CASE WHEN (COALESCE(pi.username, "") = "") THEN 0 ELSE 1 END as isPillar
                    from post p
					left join category c on p.categoryid = c.categoryid
					left join pillar pi on pi.username = %s and pi.supportUsername = p.username
                    where postid = %s""", (session["username"],str(postid),))
	post = cursor.fetchone()
	cursor.close()
	if not post:
		return json.dumps({'error':'postid not valid'})
	
	opUsername = post["username"]
	showUsername = ((post["isPillar"] == 1 or opUsername == session["username"]) or getAdminLevel() > 1)
	posterUsername = (opUsername + ("(You)" if (opUsername == session["username"]) else ("(Pillar)" if post["isPillar"] == 1 else "")) if showUsername else '')
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
	return render_template('post_view.html', title=post["summary"], dateCreatedInfo=dateInfo, description=str(post["description"])
	,  postid=str(postid), comment_section=comment_html, category = post["categoryName"]
	, posterUsernameLabelStyle=("display:auto;" if showUsername else "display:none")
	, posterUsername=posterUsername)
   
def generateUniquename(username, postid, opUsername): #make this work better in future
    name = "uniqueName" + str(username) + "-" + str(postid)
    if (username == opUsername):
        name += " (OP)"
    return name
    
def generateCommentTree(commentid, postid, opUsername): #Returns the html of the comment tree starting at commentid recursively. If commentid = 0, start with the post itself
	htmlToReturn = ""
	query = """select c.commentid, c.username, c.dateCreated, c.comment, CASE WHEN COALESCE(p.supportUsername, "") != "" THEN 1 ELSE 0 END as isPillar
					from comment c
					left join pillar p on p.username = c.username and p.supportUsername = %s
					where active = 1 and """ + ("COALESCE(parentCommentid, 0) = 0 and postid = %s" if commentid == 0 else "COALESCE(parentCommentid, 0) = %s")
	conn = mysql.connection
	cursor = conn.cursor(MySQLdb.cursors.DictCursor)
	id = 0
	id = postid if commentid == 0 else commentid
	sys.stdout.flush()
	cursor.execute(query,(session["username"],str(id),))
	comments = cursor.fetchall()
	cursor.close()
	for comment in comments:
		childrenHtml = generateCommentTree(comment["commentid"], postid, opUsername)
		display = "default" if childrenHtml != "" else "none"
		showUsername = ((comment["isPillar"] == 1 and opUsername == session["username"]) or getAdminLevel() > 1)
		commenter = comment["username"]
		commenterDisplay = (generateUniquename(commenter,postid,opUsername) if showUsername else commenter) + (" (You)" if commenter==session["username"] else ("(Pillar)" if comment["isPillar"] == 1 else "") )
		htmlToReturn += comment_template_html.format(str(comment["commentid"]), comment["comment"].encode('ascii', 'ignore'), str(comment["commentid"]), str(id), str(comment["commentid"]), str(comment["commentid"]),display,comment["dateCreated"].strftime("%m/%d/%y %I:%M%p"),commenterDisplay,childrenHtml)
		#htmlToReturn += render_template('comment_template.html', username=generateUniquename(comment["username"], postid, opUsername), dateCreated=str(comment["dateCreated"]), commentid=comment["commentid"], description=comment["comment"], comment_child_html=childrenHtml)
	return htmlToReturn
