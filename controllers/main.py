from flask import *
from extensions import mysql
import MySQLdb
import sys
from helper import *
from sets import Set

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
	
	if (is_logged_in()):
		query = """select c.commentid, c.dateCreated, c.comment, p.summary, c.postid, c.username
			from comment c
			left join post p on p.postid = c.postid
			where c.active = 1 and p.username = %s and p.active = 1 and c.username in (select username from pillar where supportUsername = %s)"""
			
		_usernameFilterSupportersValue = "0"
		if('_usernameFilterSupportersValue' in request.args):
			_usernameFilterSupportersValue = request.args.get('supporter')
		selectParams = (session['username'],session['username'])
		if ('_usernameFilterSupportersValue' in request.form):
			_usernameFilterSupportersValue = sanitize(request.form['_usernameFilterSupportersValue'])
			if (_usernameFilterSupportersValue != "0"):
				query += " and c.username = %s "
				selectParams = (session['username'],session['username'],_usernameFilterSupportersValue)
			
		supportings = {}
		supporters = {}
			
		query += """ order by c.dateCreated desc"""
		cursor = conn.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute(query, selectParams)
		comments = cursor.fetchall()
		for comment in comments:
			comment['dataCreated'] = str(comment["dateCreated"].strftime("%m/%d/%y %I:%M%p"))
			supporters[comment['username']] = ""
			
		query = """select p.postid, p.summary, p.description, p.dateCreated, p.dateLastModified, nc.ct, COALESCE(c.categoryName, 'None') as categoryName, p.username
					from post p
					left join (select COUNT(*) as ct, postid from comment where active = 1 group by postid) nc on nc.postid = p.postid
					left join category c on c.categoryid = p.categoryid
					where p.active = 1 and p.username in (select supportUsername from pillar where username = %s)"""
		
		selectParams = (session['username'],)
		if ('_categoryidFilter' in request.form and is_int(request.form['_categoryidFilter'])):
			_categoryIdFilter = sanitize(request.form['_categoryidFilter'])
			if (_categoryIdFilter == -1):
				query += " and c.categoryid is null "
			elif (_categoryIdFilter != 0):
				query += " and p.categoryid = " + str(_categoryIdFilter)
				
		_usernameFilterSupportingsValue = 0
		if('_usernameFilterSupportingsValue' in request.args):
			_usernameFilterSupportingsValue = request.args.get('supporting')
		if ('_usernameFilterSupportingsValue' in request.form):
			_usernameFilterSupportingsValue = sanitize(request.form['_usernameFilterSupportingsValue'])
			if (_usernameFilterSupportingsValue != "0"):
				query += " and p.username = %s "
				selectParams = (_usernameFilterSupportingsValue, session['username'],)
				
		query += """ order by p.dateCreated, p.dateLastModified, p.summary""";
		cursor = conn.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute(query, selectParams)
		supportingPosts = cursor.fetchall()
		for post in supportingPosts:
			post['dataCreated'] = str(post["dateCreated"].strftime("%m/%d/%y %I:%M%p"))
			supportings[post['username']] = ""
		return render_template('index.html', Posts=htmlToReturn, categories=getCategories()
			, _categoryidFilter = _categoryIdFilter, _categoryFilterName = _categoryFilterName, comments=comments
			, supportingPosts=supportingPosts, _usernameFilterSupportersValue=_usernameFilterSupportersValue, _usernameFilterSupportingsValue=_usernameFilterSupportingsValue, supportings=supportings.keys(), supporters = supporters.keys())
	else:
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
	