from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from project_dbsetup import User, Author, Work_titles, Discussion, Base
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests
import datetime

# Connect to Database and create database session
engine = create_engine('sqlite:///authorsandworktitles.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)

today = datetime.date.today()

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Thoughts Repository"


# "Helper" code to create user in database if non-existent in database
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session
                ['email'], picture_url=login_session['picture'],
                superuser="No")
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id

# "Helper" code to get specific user information from database
def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user

# "Helper" code to get specific user id from database
def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('users_signin.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius:\
    150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


@app.route('/logout')
def gdisconnect():
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        del login_session['state']
        login_session.clear()
        print login_session
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response and redirect('/home')
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/')
@app.route('/home/')
def homepage():
    if 'username' not in login_session:
        return render_template('main_pagepublic.html')
    else:
        return render_template('main_page.html', login_session=login_session)


# Show all authors that belong to "light" category
@app.route('/light')
def showlightauthors():
    authors = session.query(Author).filter_by(category="light").order_by(asc(Author.name))
    return render_template('Authors_listlight.html',
            authors=authors, login_session=login_session)


# Show all authors that belong to "light" category in JSON format
@app.route('/light/JSON/')
def showlightauthorsinJSON():
    authors = session.query(Author).filter_by(category="light").order_by(asc(Author.name))
    return jsonify(authors=[individual.serialize for individual in authors])


# Show all authors that belong to "dark" category
@app.route('/dark')
def showdarkauthors():
    authors = session.query(Author).filter_by(category="dark").order_by(asc(Author.name))
    return render_template('Authors_listdark.html',
            authors=authors, login_session=login_session)

# Show all authors that belong to "dark" category in JSON format
@app.route('/dark/JSON/')
def showlightauthorsinJSON():
    authors = session.query(Author).filter_by(category="dark").order_by(asc(Author.name))
    return jsonify(authors=[individual.serialize for individual in authors])


# Show all authors' work that belong to "light" category
@app.route('/light/<int:author_id>/')
def showlightauthorworks(author_id):
    author = session.query(Author).filter_by(id=author_id).one()
    works = session.query(Work_titles).filter_by(author_id=author_id)
    return render_template('Author_works.html',
            author=author, works=works, login_session=login_session)


# Show all authors' work that belong to "dark" category
@app.route('/dark/<int:author_id>/')
def showdarkauthorworks(author_id):
    author = session.query(Author).filter_by(id=author_id).one()
    works = session.query(Work_titles).filter_by(author_id=author_id)
    return render_template('Author_works.html',
            author=author, works=works, login_session=login_session)


# Show individual work information
@app.route('/<int:author_id>/<int:worktitle_id>/')
def showindividualwork(author_id, worktitle_id):
    author = session.query(Author).filter_by(id=author_id).one()
    work = session.query(Work_titles).filter_by(id=worktitle_id).one()
    discussions = session.query(Discussion).filter_by(work_id=worktitle_id).all()
    if 'username' not in login_session:
        return render_template('individual_workpublic.html',
                author=author, work=work, discussions=discussions,
                login_session=login_session)
    else:
        user = session.query(User).filter_by(email=login_session['email']).one()
        if user.superuser == "Yes":
            return render_template('individual_worksuperuser.html',
                    author=author, work=work, discussions=discussions,
                    login_session=login_session)
        else:
            return render_template('individual_workmember.html',
                    author=author, work=work, discussions=discussions,
                    login_session=login_session)


# Code to allow logged-in user to create new message in forum
@app.route('/<int:author_id>/<int:worktitle_id>/newmessage', methods=['GET', 'POST'])
def newmessage(author_id, worktitle_id):
    if request.method == 'POST':
        message = request.form['message']
        date = today.strftime('%d/%m/%Y')
        discussion = Discussion(message=message, date_created=date,
        user_id=login_session['user_id'], work_id=worktitle_id)
        session.add(discussion)
        session.commit()
        return redirect(url_for('showindividualwork', author_id=author_id,
                worktitle_id=worktitle_id))
    else:
        return render_template('newmessage.html')


# Code to allow super-user to edit/moderate message in forum. Before you can
# do this, ensure that you have updated the column "superuser" in the User
# table to "Yes" for the user you wish to grant administrative rights.
@app.route('/editmessage/<int:message_id>/', methods=['GET', 'POST'])
def editmessage(message_id):
    discussion = session.query(Discussion).filter_by(id=message_id).one()
    work_id = discussion.work_id
    work_title = session.query(Work_titles).filter_by(id=work_id).one()
    author_id = work_title.author_id
    if request.method == 'POST':
        updatedmessage = request.form['message']
        date = today.strftime('%d/%m/%Y')
        discussion.message = updatedmessage
        session.add(discussion)
        session.commit()
        return redirect(url_for('showindividualwork', author_id=author_id,
                worktitle_id=work_id))
    else:
        return render_template('editmessage.html', message_id=message_id)


# Code to allow super-user to delete message in forum. Before you can
# do this, ensure that you have updated the column "superuser" in the User
# table to "Yes" for the user you wish to grant administrative rights.
@app.route('/deletemessage/<int:message_id>/', methods=['GET', 'POST'])
def deletemessage(message_id):
    discussion = session.query(Discussion).filter_by(id=message_id).one()
    work_id = discussion.work_id
    work_title = session.query(Work_titles).filter_by(id=work_id).one()
    author_id = work_title.author_id
    if request.method == 'POST':
        session.delete(discussion)
        session.commit()
        return redirect(url_for('showindividualwork', author_id=author_id,
                worktitle_id=work_id))
    else:
        return render_template('deletemessage.html', message_id=message_id)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
