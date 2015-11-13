from flask import *
from extensions import mysql
import MySQLdb

post_create = Blueprint('post_create', __name__)

@post_create.route('/')
def post_route():
    return render_template('base.html')

@post_create.route('/',methods=['POST'])
def signUp():
    try:
        _userid = 1 #TD: Add in login function/check
        _summary = request.form['_summary']
        _description = request.form['_description']

        # validate the received values
        if _userid and _summary and _description:
            
            # All Good, let's call MySQL
            
            conn = mysql.connect()
            cursor = conn.cursor()
			cursor.execute("insert into post (userid, summary, description, dateCreated, dateLastModified, active) values (%s, %s, %s, GETDATE(), GETDATE(), 1)", (_userid, _summary, _description))
            cursorid = cursor.lastrowid

            if cursorid is not 0:
                conn.commit()
                return json.dumps({'message':'Post created successfully !'})
            else:
                return json.dumps({'error':"Post could not be created: " + str(data[0])})
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close() 
        conn.close()