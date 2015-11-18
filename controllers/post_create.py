from flask import *
from extensions import mysql
from helper import *
import MySQLdb
import MySQLdb.cursors

post_create = Blueprint('post_create', __name__,template_folder='views')

@post_create.route('/post/create',methods=['GET'])
def post_route():
    if not is_logged_in():
        return render_template('user_login.html')    
    return render_template('post_create.html')

@post_create.route('/post/create',methods=['POST'])
def create():
    if not is_logged_in():
        return render_template('user_login.html')

    try:
        _username = session['username'] #TD: Add in login function/check
        _summary = request.form['_summary']
        _description = request.form['_description']

        # validate the received values
        if _username and _summary and _description:
            
            # All Good, let's call MySQL
            conn = mysql.connection
            cursor = conn.cursor()
            cursor.execute("insert into post (username, summary, description) values (%s, %s, %s)", (_username, _summary, _description))

            cursorid = cursor.lastrowid

            if cursorid is not 0:
                conn.commit()
                return redirect(url_for('post_view.show_post') + "?postid=" + cursorid)
            else:
                return json.dumps({'error':"Post could not be created: "})
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error':str(e)})