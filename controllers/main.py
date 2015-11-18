from flask import *
from extensions import mysql
import MySQLdb

main = Blueprint('main', __name__)

@main.route('/')
def main_route():
	post_template_html = open('views/post_template.html', 'r').read()
	htmlToReturn = ""
	query = """select p.postid, summary, description, dateCreated, dateLastModified, nc.ct
				from post p
				left join (select COUNT(*) as ct, postid from comment where active = 1 group by postid) nc on nc.postid = p.postid
				where p.active = 1 order by dateCreated, dateLastModified, summary""";
	conn = mysql.connection
	cursor = conn.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute(query)
	post = cursor.fetchone()
	while(post):
		_dateInfo = str(post["dateCreated"].strftime("%m/%d/%y %I:%M%p"))
		dateLastModified = post["dateLastModified"]
		if(dateLastModified and dateLastModified != post["dateCreated"]):
			_dateInfo += " (edited on " + str(dateLastModified.strftime("%m/%d/%y %I:%M%p")) + ")"
		htmlToReturn += post_template_html.format(url_for('post_view.show_post') + "?postid=" + str(post["postid"]), post["summary"],post["description"],_dateInfo,post["ct"] )
		#htmlToReturn += render_template('post_template.html', postid=post["postid"], title=post["summary"], description=post["description"],dateInfo=_dateInfo)
		post = cursor.fetchone()
	cursor.close()
	return render_template('index.html', Posts=htmlToReturn)
