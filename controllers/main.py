from flask import *
from extensions import mysql
import MySQLdb

main = Blueprint('main', __name__)

@main.route('/')
def main_route():
    # conn = mysql.connection
    # cur = conn.cursor(MySQLdb.cursors.DictCursor)
    # cur.execute("SELECT * FROM USER WHERE USERNAME='%s'" % 'luochen');
    # user = cur.fetchone()
    # username = user['username']
    # email = user['email']
    return render_template('base.html')
