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

user = Blueprint('user', __name__, template_folder='views')

# All helper functions
def get_token(username):
    serializer = URLSafeSerializer(config.SECRET_KEY)
    return serializer.dumps(username)

def get_new_password():
    return ''.join(random.choice(string.lowercase + string.digits) for i in range(5))

class EmailSender:
    VERIFICATION = 'verification'
    FORGET_PASSWORD = 'forget_password'
    def __init__(self, action, email=None, new_password=None):
        self.action = action
        self.email = email
        self.new_password = new_password

    def send_email(self):
        @copy_current_request_context
        def send_email(msg):
            mail.send(msg)
        if self.action == self.VERIFICATION:
            sender = threading.Thread(name='mail_sender', target=send_email, args=(self.create_verification_email(),))
        elif self.action == self.FORGET_PASSWORD:
            sender = threading.Thread(name='mail_sender', target=send_email, args=(self.create_forget_password_email(),))
        sender.start()

    def create_verification_email(self):
        msg = Message('Please Verify', sender="eecs485.group3@gmail.com")
        msg.recipients = [request.form['email']]
        msg.html = render_template("email_verification.html", token=get_token(request.form['username']))
        return msg

    def create_forget_password_email(self):
        msg = Message('New Password', sender="eecs485.group3@gmail.com")
        msg.recipients = [self.email]
        msg.html = render_template("email_forget_password.html", new_password=self.new_password)
        return msg

@user.route('/user/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'GET' and 'username' not in session:
        return render_template('user_login.html', prev_url=request.args.get('url'))
    elif request.method == 'GET' and 'username' in session:
        return redirect(url_for('main.main_route'))
    else:
        # Check if user exists and if password is correct
        conn = mysql.connection
        cur = conn.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM USER WHERE USERNAME='%s'" % request.form['username'])
        user = cur.fetchone()
        if user is None:
            flash('Username does not exist!')
            return render_template('user_login.html', prev_url=request.args.get('url'))
        elif user['CONFIRMED'] == 0:
            flash('Your account is not activated. Please click the link in email')
            return render_template('user_login.html', prev_url=request.args.get('url'))

        # Forget password or password is not correct
        if 'forget_password'in request.form:
            flash('The new password has been generated and sent to your email.')
            new_password = get_new_password()
            new_password_hash = hashlib.md5(new_password).hexdigest()
            cur.execute("UPDATE USER SET PASSWORD='%s' WHERE USERNAME='%s'" % (new_password_hash, user['USERNAME']))
            conn.commit()
            email_sender = EmailSender(EmailSender.FORGET_PASSWORD, user['EMAIL'], new_password)
            email_sender.send_email()
            return render_template('user_login.html', prev_url=request.args.get('url'))
        elif hashlib.md5(request.form['password']).hexdigest() != user['PASSWORD']:
            flash('Wrong password! Please try again')
            return render_template('user_login.html', prev_url=request.args.get('url'))

        # Set up the session
        session['username'] = request.form['username']
        update_last_activity()

        # Redirect to prev url or the main page
        if request.form['prev_url'] != "None":
            return redirect(request.form['prev_url'])
        else:
            return redirect(url_for('main.main_route'))

@user.route('/logout', methods=['GET'])
def user_logout():
    destroy_session()
    return redirect(url_for('main.main_route'))

@user.route('/user', methods=['GET','POST'])
def user_register():
    if request.method == 'GET' and is_logged_in():
        return redirect(url_for('.user_edit'))
    if request.method == 'GET':
        # return the register page
        return render_template('user_register.html')
    else:
        # check if two passwords match
        if (request.form['password'] != request.form['password_confirm']):
            flash("Password must match!")
            return render_template('user_register.html')

        # check if username already exists
        conn = mysql.connection
        cur = conn.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM USER WHERE USERNAME='%s'" % request.form['username'])
        res = cur.fetchall()
        if (len(res) >= 1):
            flash('Username already exists!')
            return render_template('user_register.html')

        # insert the user to database
        password_hash = hashlib.md5(request.form['password']).hexdigest()
        cur.execute("INSERT INTO USER (USERNAME, PASSWORD, FIRSTNAME, LASTNAME, EMAIL) "
                    "VALUES ('%s', '%s', '%s', '%s', '%s')" % (request.form['username'],
                    password_hash, request.form['firstname'], request.form['lastname'], request.form['email']))
        conn.commit()

        # send verification email
        email_sender = EmailSender(EmailSender.VERIFICATION)
        email_sender.send_email()
        flash('An email has been sent. Please click the link in the email to verify your account')
        return redirect(url_for('main.main_route'))

@user.route('/user/edit', methods=['GET', 'POST'])
def user_edit():
    if not is_logged_in():
        return redirect(url_for('user.user_login'))

    conn = mysql.connection
    cur = conn.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM USER WHERE USERNAME='%s'" % session['username'])
    user = cur.fetchone()
    if request.method == 'GET':
        # Populate the existing data
        update_last_activity()
        print user
        return render_template('user_edit.html', user=user)
    else:
        if request.form['password'] != request.form['password_confirm']:
            flash('Password must match')
            return render_template('user_edit', user=user)
        password = hashlib.md5(request.form['password']).hexdigest()
        cur.execute("UPDATE USER SET PASSWORD='%s', EMAIL='%s', FIRSTNAME='%s', LASTNAME='%s' WHERE USERNAME='%s'"
                    % (password, request.form['email'], request.form['firstname'], request.form['lastname'], session['username']))
        conn.commit()
        update_last_activity()
        return redirect(url_for('main.main_route'))

@user.route('/user/delete', methods=['GET'])
def user_delete():
    if not is_logged_in():
        return redirect(url_for('user.user_login'))

    conn = mysql.connection
    cur = conn.cursor(MySQLdb.cursors.DictCursor)

    # delete user
    cur.execute("DELETE FROM USER WHERE USERNAME='%s'" % session['username'])
    conn.commit()

    # destroy session
    destroy_session()
    return redirect(url_for('main.main_route'))

@user.route('/confirm', methods=['GET'])
def user_confirm():
    token = request.args.get('token')
    serializer = URLSafeSerializer(config.SECRET_KEY)
    if token is None:
        return "404 Not Found"
    username = serializer.loads(token)
    print username
    conn = mysql.connection
    cur = conn.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM USER WHERE USERNAME='%s' AND CONFIRMED=0" % username)
    user = cur.fetchone()
    if user is None:
        return "404 Not Found"
    cur.execute("UPDATE USER SET CONFIRMED=1 WHERE USERNAME='%s'" % username)
    conn.commit()

    # Login user and set up session
    session['username'] = username
    update_last_activity()
    return redirect(url_for('main.main_route'))

