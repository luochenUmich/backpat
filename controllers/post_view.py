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
		flash (json.dumps({'error':'postid not specified'}))
		return redirect(redirect_url(request))
	postid = request.args.get('postid')
	showInactiveComments = False
	if ('showInactiveComments' in request.args):
		showInactiveComments = (request.args.get('showInactiveComments') == "1") and getAdminLevel() >= 2
	conn = mysql.connection
	cursor = conn.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute("""select p.username, p.summary, p.description, p.dateCreated, p.dateLastModified, c.categoryName, CASE WHEN (COALESCE(pi.username, "") = "") THEN 0 ELSE 1 END as isPillar, p.active
                    from post p
					left join category c on p.categoryid = c.categoryid
					left join pillar pi on pi.username = %s and pi.supportUsername = p.username
                    where postid = %s""", (session["username"],str(postid),))
	post = cursor.fetchone()
	cursor.close()
	if not post:
		flash(json.dumps({'error':'postid not valid'}))
		return redirect(redirect_url(request))
	
	opUsername = post["username"]
	showUsername = ((post["isPillar"] == 1 or opUsername == session["username"]) or getAdminLevel() > 1)
	posterUsername = (opUsername + ("(You)" if (opUsername == session["username"]) else ("(Pillar)" if post["isPillar"] == 1 else "")) if showUsername else '')
    #Get all the comments
	global comment_template_html
	comment_template_html = open('views/comment_template.html', 'r').read()
	comment_html = generateCommentTree(0, postid, opUsername, showInactiveComments)
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
	, posterUsername=posterUsername
	, checkbox_redirect_url=url_for("post_view.show_post") + "?postid=" + postid + "&showInactiveComments=" + ("0" if showInactiveComments else "1")
	, isChecked="checked"if showInactiveComments else ""
	, removeTextPost="Remove"if post["active"]==1 else "Deleted"
	, removePostDisplay="default"if opUsername == session["username"] or getAdminLevel() >=2 else "none")
   
def generateUniquename(username, postid, opUsername): #make this work better in future
    name = "uniqueName" + str(username) + "-" + str(postid)
    if (username == opUsername):
        name += " (OP)"
    return name
    
def generateCommentTree(commentid, postid, opUsername, showInactiveComments): #Returns the html of the comment tree starting at commentid recursively. If commentid = 0, start with the post itself
	htmlToReturn = ""
	query = """select c.commentid, c.username, c.dateCreated, c.comment, CASE WHEN COALESCE(p.supportUsername, "") != "" THEN 1 ELSE 0 END as isPillar, c.active
					from comment c
					left join pillar p on p.username = c.username and p.supportUsername = %s
					where """ + ("" if showInactiveComments else "c.active = 1 and ") + ("COALESCE(parentCommentid, 0) = 0 and postid = %s" if commentid == 0 else "COALESCE(parentCommentid, 0) = %s")
	conn = mysql.connection
	cursor = conn.cursor(MySQLdb.cursors.DictCursor)
	id = 0
	id = postid if commentid == 0 else commentid
	sys.stdout.flush()
	cursor.execute(query,(session["username"],str(id),))
	comments = cursor.fetchall()
	cursor.close()
	displayRemoveComment = "default" if getAdminLevel() >= 2 or opUsername == session["username"] else "none"
	for comment in comments:
		childrenHtml = generateCommentTree(comment["commentid"], postid, opUsername, showInactiveComments)
		display = "default" if childrenHtml != "" else "none"
		showUsername = ((comment["isPillar"] == 1 and opUsername == session["username"]) or getAdminLevel() > 1)
		commenter = comment["username"]
		removeTextComment = "Remove" if comment["active"] == 1 else "DELETED"
		commenterDisplay = (generateUniquename(commenter,postid,opUsername) if showUsername else commenter) + (" (You)" if commenter==session["username"] else ("(Pillar)" if comment["isPillar"] == 1 else "") )
		htmlToReturn += comment_template_html.format(str(comment["commentid"]), comment["comment"].encode('ascii', 'ignore')
		, str(comment["commentid"]), str(id), str(comment["commentid"])
		, str(comment["commentid"]), str(comment["commentid"]), displayRemoveComment, removeTextComment
		,display,comment["dateCreated"].strftime("%m/%d/%y %I:%M%p"),commenterDisplay,childrenHtml)
		#htmlToReturn += render_template('comment_template.html', username=generateUniquename(comment["username"], postid, opUsername), dateCreated=str(comment["dateCreated"]), commentid=comment["commentid"], description=comment["comment"], comment_child_html=childrenHtml)
	return htmlToReturn
	
@post_view.route('/post/remove_item', methods=["POST"])
def remove_item():
	if not is_logged_in():
		return render_template('user_login.html')
	if 'postid' not in request.args:
		flash (json.dumps({'error':'postid not specified'}))
		return redirect(redirect_url(request))
	postid = request.args.get('postid')
	commentid = 0
	if ('_commentidRemove' in request.form and is_int(request.form["_commentidRemove"])):
		commentid = int(request.form["_commentidRemove"])
	banUser = False
	if ('banUser' in request.form and is_int(request.form["_banUser"]) and int(request.form["_banUser"]) == 1 and getAdminLevel() >= 2):
		banUser = True
	conn = mysql.connection
	cursor = conn.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute("""select p.username, p.active, c.username as commenter, c.active as commentActive
                    from post p
					left join comment c on c.postid = p.postid and c.commentid = %s
                    where p.postid = %s""", (commentid,str(postid),))
	post = cursor.fetchone()
	cursor.close()
	if not post:
		flash(json.dumps({'error':'postid not valid'}))
		return redirect(redirect_url(request))
	if (commentid != 0 and not post["commenter"]):
		flash(json.dumps({'error':'commentid not valid for this post'}))
		return redirect(redirect_url(request))
	if (post["username"] != session["username"] and getAdminLevel() < 2):
		flash("You do not have permission to use this function")
		return redirect(redirect_url(request))
	if (post["commenter"]):
		cursor = conn.cursor()
		cursor.execute("update comment set active = 0 where commentid = %s", (commentid,))
		cursor.close()
		flash("Comment deleted")
		if (banUser): 
			cursor = conn.cursor()
			cursor.execute("update user set active = 0 where username = %s", (post["commenter"],))
			cursor.close()
			flash("User banned")
		conn.commit()
	else:
		cursor = conn.cursor()
		cursor.execute("update post set active = 0 where postid = %s", (postid,))
		cursor.close()
		flash("Post deleted")
		if (banUser):
			cursor = conn.cursor()
			cursor.execute("update user set active = 0 where username = %s", (post["username"],))
			cursor.close()
			flash("User banned")
		conn.commit()
	
	return redirect(redirect_url(request))