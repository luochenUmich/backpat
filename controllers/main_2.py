from flask import *
from extensions import mysql
import MySQLdb
import MySQLdb.cursors

main2 = Blueprint('main2', __name__)

@main2.route('/')
def post_route():
    htmlToReturn = ""
    query = """select p.postid, summary, description, dateCreated, dateLastModified, nc.ct [numComments]
                from post p
                left join (select COUNT(*) ct, postid from comment where active = 1 group by postid) nc on nc.postid = p.postid
                where p.active = 1 order by dateCreated, dateLastModified, summary""";
    conn = mysql.connect()
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(query)
    post = cursor.fetchone()
    while(comment):
        _dateInfo = str(post["dateCreated"])
        dateLastModified = post["dateLastModified"]
        if(dateLastModified and dateLastModified != post["dateCreated"]):
            _dateInfo += " (edited on " + str(dateLastModified) + ")"
        htmlToReturn += render_template('post_template.html', postid=post["postid"], title=post["summary"], description=post["description"],dateInfo=_dateInfo)
        post = cursor.fetchone()
    conn.close()
    cursor.close()
    return render_template('main2.html', Posts=htmlToReturn)