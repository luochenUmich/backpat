from flask import *
from extensions import mysql
import MySQLdb

post_view = Blueprint('post_view', __name__)

@post_view.route('/')
def post_view_route():
    return "Error, you must enter a post number";
	
@post_view.route('/<int:postid>'))
def show_post(post_id):
	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.execute("""select top 1 userid, summary, description. dateCreated, dateLastModified, p.ct [numComments]
					from post p
					left join (select COUNT(*)[ct] from comment where postid = %s and active = 1 group by postid) nc on nc.postid = p.postid
					where postid = %s""", (post_id))
	post = cursor.fetchone()
	
	opUserid = post["userid"]
	#Get all the comments
	comment_html = generateCommentTree(0, post_id, opUserid)
	
	dateInfo = str(post["dateCreated"])
	if (post["dateLastModified"] && post["dateCreated"] != post["dateLastModified"]):
		dateInfo += "Last Modified: " + str(post["dateLastModified"])
	name = generateUniquename(userid, postid, opUserid)
	
	post_html = render_template('post_view_post_template.html', title=post["summary"], uniqname=name, dateCreatedInfo=dateInfo, numComments=post["numComments"], description=post["comments"]])
	
	conn.close()
	cursor.close()
	return render_template('post_view_template.html', post=post_html, commentSection=comment_html)
	
def generateUniquename(userid, postid, opUserid): #make this work better in future
	name = "uniqueName" + str(userid) + "-" + str(postid)
	if (userid == opUserid):
		name += " (OP)"
	return name
	
def generateCommentTree(commentid, postid, opUserid): #Returns the html of the comment tree starting at commentid recursively. If commentid = 0, start with the post itself
	htmlToReturn = ""
	query = """select commentid, userid, dateCreated, comment, CASE WHEN parentCommentid = 0 THEN 1 ELSE 0 END [expanded] from comment where active = 1 and """ + ("COALESCE(parentCommentid, 0) = 0 and postid = %s" if commentid == 0 else "parentCommentid = %s")
	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.execute(query, (postid) if commentid == 0 else (commentid))
	comment = cursor.fetchone()
	while(comment):
		childrenHtml = generateCommentTree(comment["commentid"], postid)
		htmlToReturn += render_template('comment_template.html', username=generateUniquename(comment["userid"], postid), dateCreated=str(comment["dateCreated"]), commentid=comment["commentid"], description=comment["comment"], comment-child-html=childrenHtml)
		comment = cursor.fetchone()
	conn.close()
	cursor.close()
	return htmlToReturn
	

@post_view.route('/<int:postid>',methods=['POST'])
def makeComment(postid):
    try:
        _userid = 1 #TD: Add in login function/check
        _comment = request.form['_comment'] #text of the comment
        _parentCommentid = request.form['_parentCommentid'] #Make 0 to be reply to post

        # validate the received values
        if postid and _userid and _comment and _parentCommentid:
            # All Good, let's call MySQL
            conn = mysql.connect()
            cursor = conn.cursor()
			cursor.execute("""insert into comment (postid, parentCommentid, userid, active, dateCreated, comment) values (%s, %s, %s, 1, GETDATE(), %s)""", (_postid, _parentCommentid, _userid, _comment))
            commentid = cursor.lastrowid

            if commentid is not 0:
                conn.commit()
                return json.dumps({'message':'Comment created successfully !'})
            else:
                return json.dumps({'error':"Comment could not be created: " + str(data[0])})
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close() 
        conn.close()