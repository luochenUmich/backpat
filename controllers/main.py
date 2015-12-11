from flask import *
from extensions import mysql
import MySQLdb
import sys
from helper import *

main = Blueprint('main', __name__)

@main.route('/', methods=['POST','GET'])
def main_route():
	post_template_html = open('views/post_template.html', 'r').read()
	htmlToReturn = ""
	
	_categoryIdFilter = 0
	_categoryFilterName = "Show All"
	
	query = """select p.postid, p.summary, p.description, p.dateCreated, p.dateLastModified, nc.ct, COALESCE(c.categoryName, 'None') as categoryName 
				from post p
				left join (select COUNT(*) as ct, postid from comment where active = 1 group by postid) nc on nc.postid = p.postid
				left join category c on c.categoryid = p.categoryid
				where p.active = 1 """
	
	if ('_categoryidFilter' in request.form and is_int(request.form['_categoryidFilter'])):
		_categoryIdFilter = int(sanitize(request.form['_categoryidFilter']))
		if (_categoryIdFilter == -1):
			query += " and c.categoryid is null "
			_categoryFilterName = "None"
		elif (_categoryIdFilter != 0):
			query += " and p.categoryid = " + str(_categoryIdFilter)
			_categoryFilterName = getCategoryName(_categoryIdFilter)
			
	query += """ order by p.dateCreated, p.dateLastModified, p.summary""";
	
	conn = mysql.connection
	cursor = conn.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute(query)
	post = cursor.fetchone()
	while(post):
		_dateInfo = str(post["dateCreated"].strftime("%m/%d/%y %I:%M%p"))
		dateLastModified = post["dateLastModified"]
		if(dateLastModified and dateLastModified != post["dateCreated"]):
			_dateInfo += " (edited on " + str(dateLastModified.strftime("%m/%d/%y %I:%M%p")) + ")"
		htmlToReturn += post_template_html.format(url_for('post_view.show_post') + "?postid=" + str(post["postid"]), post["summary"],post["description"],post["categoryName"],_dateInfo,post["ct"] )
		post = cursor.fetchone()
	cursor.close()
	return render_template('index.html', Posts=htmlToReturn, categories=getCategories(), _categoryidFilter = _categoryIdFilter, _categoryFilterName = _categoryFilterName)

def getCategories():
	categories = ""
	query = """select categoryid, categoryName
				from category
				where active = 1 order by categoryName""";
	conn = mysql.connection
	cursor = conn.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute(query)
	category = cursor.fetchone()
	while(category):
		categories += ("""<li role="presentation" value=\"""" + str(category["categoryid"]) + """""><a role="menuitem" tabindex="-1" href="#">""" + category["categoryName"] + """</a></li>""")
		category = cursor.fetchone()
	cursor.close()
	return categories
	
def getCategoryName(categoryid):
	rVal = ""
	query = """select categoryName
				from category
				where active = 1 and categoryid = %s""";
	conn = mysql.connection
	cursor = conn.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute(query, (categoryid,))
	category = cursor.fetchone()
	while(category):
		rVal = category["categoryName"]
		category = cursor.fetchone()
	cursor.close()
	return rVal
	