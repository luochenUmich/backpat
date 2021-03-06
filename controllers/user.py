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

@user.route('/user/login', methods=['GET', 'POST'])
def user_login():
    if "username" in request.form:
        print('Username: ' + request.form['username'])
    if request.method == 'GET' and 'username' not in session:
        return render_template('user_login.html')
    elif request.method == 'GET' and 'username' in session:
        return redirect(url_for('main.main_route'))
    else:
        # Check if user exists and if password is correct
        conn = mysql.connection
        cur = conn.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM user WHERE USERNAME=%s" , (sanitize(request.form['username']),))
        print("SELECT * FROM user WHERE USERNAME=%s" , (sanitize(request.form['username']),))
        user = cur.fetchone()
        if user is None:
            flash('Username does not exist!')
            return render_template('user_login.html')

        # Forget password or password is not correct
        if hashlib.md5(sanitize(request.form['password'])).hexdigest() != user['password']:
            flash('Wrong password! Please try again')
            return render_template('user_login.html', prev_url=request.args.get('url'))
            
        #If user is banned, redirect them to you've been banned screen
        if user['active'] != 1:
            flash('You have been banned!')
            return render_template('user_login.html', prev_url=request.args.get('url'))

        # Set up the session
        session['username'] = sanitize(request.form['username'])
        session['adminLevel'] = user['adminLevel']
        return redirect(url_for('main.main_route'))

@user.route('/logout', methods=['GET'])
def user_logout():
    destroy_session()
    return redirect(url_for('main.main_route'))

@user.route('/user', methods=['GET','POST'])
def user_register():
    if request.method == 'GET':
        # return the register page
        return render_template('user_register.html')
    else:
        # check if two passwords match
        if (sanitize(request.form['password']) != sanitize(request.form['password_confirm'])):
            flash("Password must match!")
            return render_template('user_register.html')

        # check if username already exists
        conn = mysql.connection
        cur = conn.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM user WHERE USERNAME='%s'" % sanitize(request.form['username']))
        res = cur.fetchall()
        if (len(res) >= 1):
            flash('Username already exists!')
            return render_template('user_register.html')

        # insert the user to database
        password_hash = hashlib.md5(sanitize(request.form['password'])).hexdigest()
        cur.execute("INSERT INTO user (USERNAME, PASSWORD, EMAIL, ADMINLEVEL) "
                    "VALUES ('%s', '%s', '%s', 0)" % (sanitize(request.form['username']),
                    password_hash, sanitize(request.form['email'])))
        conn.commit()

        session['username'] = sanitize(request.form['username'])
        session['adminlevel'] = 0
        return redirect(url_for('main.main_route'))

@user.route('/profile', methods=['GET'])
def user_profile():
    if 'username' not in session:
        return render_template('user_login.html')
    else:
        #User Info
        query = """select u.email, CASE WHEN u.adminLevel >= 2 THEN 'Administrator' WHEN u.adminLevel >= 1 THEN 'Moderator' ELSE 'Normal User' END as adminLevelText, CASE WHEN u.active then 'Active' else 'Inactive' end as status, u.created_at
                from user u
                where u.username = %s"""
        conn = mysql.connection
        cur = conn.cursor(MySQLdb.cursors.DictCursor)
        cur.execute(query, (session['username'],))
        user = cur.fetchone()
        
        #Posts
        query = """select p.postid, summary, description, dateCreated, dateLastModified, nc.ct
                from post p
                left join (select COUNT(*) as ct, postid from comment where active = 1 group by postid) nc on nc.postid = p.postid
                where p.active = 1 and username = %s order by dateCreated desc, dateLastModified, summary"""
        cur.execute(query, (session['username'],))
        posts = cur.fetchall()
        for post in posts:
            post['dataCreated'] = str(post["dateCreated"].strftime("%m/%d/%y %I:%M%p"))

        #Comments you've made
        query = """select c.commentid, c.dateCreated, c.comment, p.summary, c.postid
                from comment c
                left join post p on p.postid = c.postid
                where c.username = %s"""
        cur.execute(query, (session['username'],))
        comments = cur.fetchall()
        for comment in comments:
            comment['dataCreated'] = str(comment["dateCreated"].strftime("%m/%d/%y %I:%M%p"))
            
        #Supporters you have
        query = """select p.username, p.dateCreated, ci.postid, ci.comment, ci.summary
                    from pillar p
                    left join (select c.username, c.dateCreated, c.comment, c.postid, c.summary
                        from (select cSub.username, cSub.dateCreated, cSub.comment,po.postid, po.summary from comment cSub left join post po on po.postid = cSub.postid and po.active = 1 and cSub.active = 1 and po.username = %s) c 
						left join (select cSub.username, cSub.dateCreated, cSub.comment,po.postid, po.summary from comment cSub left join post po on po.postid = cSub.postid and po.active = 1 and cSub.active = 1 and po.username = %s) c2 on c2.username = c.username and c2.dateCreated > c.dateCreated
                        where c2.username is null) ci on ci.username = p.username
                    where p.supportUsername = %s"""
        cur.execute(query, (session['username'],session['username'],session['username']))
        supporters = cur.fetchall()
        numSupporters = cur.rowcount
        for supporter in supporters:
            supporter['dataCreated'] = str(supporter["dateCreated"].strftime("%m/%d/%y %I:%M%p"))
            
        #People you are supporting
        query = """select p.supportUsername as username, p.dateCreated, pi.postid, pi.summary
                    from pillar p
                    left join (	
						select po.username,po.postid, po.summary
						from post po 
						left join post po2 on po2.username = po.username and po2.dateCreated > po.dateCreated
						where po.active = 1 and po2.username is null) pi on pi.username = p.supportUsername
                    where p.username = %s"""
        cur.execute(query, (session['username'],))
        supportings = cur.fetchall()
        numSupportings = cur.rowcount
        for supporting in supportings:
            supporting['dataCreated'] = str(supporting["dateCreated"].strftime("%m/%d/%y %I:%M%p"))
            
        #Pillar Requests as description
        query = """select requestedByUsername, pr.reason, pr.dateCreated, CASE WHEN pr.isTwoWay = 1 THEN 'Requesting and Offering Support' WHEN pr.username = %s THEN 'Requesting Support' ELSE 'Offering Support' END as description
                    from pillar_request pr
                    where requestedByUsername != %s and (username = %s or supportUsername = %s) and dateAccepted < 19700101"""
        cur.execute(query, (session['username'],session['username'],session['username'],session['username']))
        pillarRequests = cur.fetchall()
        numPillarRequests = cur.rowcount
        for pillarRequest in pillarRequests:
            pillarRequest['dataCreated'] = str(pillarRequest["dateCreated"].strftime("%m/%d/%y %I:%M%p"))
            
        cur.close()
            
        return render_template('user_profile.html', username=session['username'], registered_on=user['created_at'], adminLevel=user['adminLevelText'], email=user['email'], status=user['status'], posts=posts, comments=comments, pillarRequests=pillarRequests, supporters=supporters, supportings=supportings,numSupporters=numSupporters, numSupporting=numSupportings,  numRequests=numPillarRequests)

@user.route('/user/delete', methods=['GET'])
def user_delete():
    if not is_logged_in():
        return redirect(url_for('user.user_login'))

    conn = mysql.connection
    cur = conn.cursor(MySQLdb.cursors.DictCursor)

    # delete user
    cur.execute("DELETE FROM user WHERE USERNAME='%s'" % session['username'])
    conn.commit()

    # destroy session
    destroy_session()
    return redirect(url_for('main.main_route'))

