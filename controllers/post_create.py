from flask import *
from extensions import mysql
import MySQLdb

post_create = Blueprint('post_create', __name__)

@post_create.route('/')
def post_route():
	if not is_logged_in():
		return render_template('user_login.html')
    return render_template('post_create.html')

@post_create.route('/',methods=['POST'])
def signUp():
    if not is_logged_in():
		return render_template('user_login.html')
    try:
        _username = session['username'] #TD: Add in login function/check
        _summary = request.form['_summary']
        _description = request.form['_description']

        # validate the received values
        if _username and _summary and _description:
            
            # All Good, let's call MySQL
            
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute("insert into post (username, summary, description) values (%s, %s, %s)", (_username, _summary, _description))
            cursorid = cursor.lastrowid

            if cursorid is not 0:
                conn.commit()
                return redirect(url_for('post_view.post_view_route'))
            else:
                return json.dumps({'error':"Post could not be created: ")})
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close() 
        conn.close()