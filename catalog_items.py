from flask import Flask, render_template, request, redirect, url_for, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, Item, User

from flask import session as login_session
import random
import string

from flask import flash

# IMPORTS FOR THIS STEP
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Item Catalog App"

engine = create_engine('sqlite:///catalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()

# Create anti-forgery state token


@app.route('/')
def login():
    """ This is the home page of application which allows user to login """
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


@app.errorhandler(Exception)
def page_not_found(e):
    return render_template('error.html', message=e.message)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    """ This is a method which helps in google sign-in """
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
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
            'Current user is already connected.'), 200)
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

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style =+\
    "width: 300px; height: 300px;border-radius: 150px;" +\
    "-webkit-border-radius: 150px;-moz-border-radius: 150px;" > '
    flash("you are now logged in as %s" % login_session['username'])
    return output


@app.route('/gdisconnect')
def gdisconnect():
    """ This method is invoked when the user clicks on signout
    This disconnects the user and clears the session data """
    if login_session['userid']:
        del login_session['username']
        del login_session['userid']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return redirect(url_for('login'))
    elif login_session['access_token']:
        url = 'https://accounts.google.com/o/oauth2/' +\
            'revoke?token=%s' % login_session['access_token']
        h = httplib2.Http()
        result = h.request(url, 'GET')[0]
        if result['status'] == '200':
            del login_session['access_token']
            del login_session['gplus_id']
            del login_session['username']
            del login_session['email']
            del login_session['picture']
            response = make_response(
                json.dumps('Successfully disconnected.'), 200)
            response.headers['Content-Type'] = 'application/json'
            return redirect(url_for('login'))
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/login', methods=['POST'])
def userLogin():
    """ This method authenticates the app user """
    # message=""
    session = DBSession()
    try:
        user = session.query(User).filter_by(
            name=request.form['username']).one()
        if user.password == request.form['password']:
            login_session['username'] = user.name
            login_session['userid'] = user.id
            return redirect(url_for('listCatalog'))
        else:
            return render_template(
                'login.html',
                message='Invalid Password! Please login again')
    except BaseException:
        return render_template(
            'login.html', message='Error fetching user details')


@app.route('/catalog')
def listCatalog():
    """ This method displays the list of categories and latest added items """
    session = DBSession()
    categories = session.query(Category).all()
    items = session.query(Item).order_by(Item.id.desc()).limit(10)
    # Create anti-forgery state token
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('list.html',
                           categories=categories, items=items, STATE=state)


@app.route('/catalog.json')
def jsonEndPoint():
    """ This handler is a json end point for all the items in the catalog """
    session = DBSession()
    items = session.query(Item).all()
    return jsonify(Item=[i.serialize for i in items])


@app.route('/catalog/<string:category_name>/items')
def itemById(category_name):
    """ This handler displays the details of items in a selected category """
    session = DBSession()
    categories = session.query(Category).all()
    category = session.query(Category).filter_by(name=category_name).one()
    items = session.query(Item).filter_by(category_id=category.id)
    return render_template('items.html',
                           category=category, items=items,
                           categories=categories)


@app.route('/catalog/<string:category_name>/items.json')
def itemByIdJson(category_name):
    """ This handler is a json end point to display
    the details of items in a selected category """
    session = DBSession()
    categories = session.query(Category).all()
    category = session.query(Category).filter_by(name=category_name).one()
    items = session.query(Item).filter_by(category_id=category.id)
    return jsonify(Item=[i.serialize for i in items])


@app.route('/catalog/<string:category_name>/<string:item_name>')
def itemDetail(category_name, item_name):
    """ This handler displays the item details on selecting an item """
    session = DBSession()
    item = session.query(Item).filter_by(name=item_name).one()
    return render_template('detail.html', item=item)


@app.route('/catalog/<string:category_name>/<string:item_name>/detail.json')
def itemDetailJson(category_name, item_name):
    """ This handler is a JSON end point to display the
    item details on selecting an item """
    session = DBSession()
    # category = session.query(Category).filter_by(name=category_name).one()
    item = session.query(Item).filter_by(name=item_name).one()
    return jsonify(item.serialize)


@app.route('/catalog/add', methods=['GET', 'POST'])
def itemAdd():
    """ This handler is invoked for adding an item """
    if login_session['userid']:
        if request.method == 'POST':
            session = DBSession()
            newItem = Item(name=request.form['name'],
                           description=request.form['description'],
                           category_id=request.form['categories'],
                           user_id=login_session['userid'])
            session.add(newItem)
            session.commit()
            return redirect(url_for('listCatalog'))
        else:
            return render_template('add.html')
    else:
        return render_template(
            'error.html',
            message="You are not authorized to view this page!")


@app.route('/catalog/<string:item_name>/edit', methods=['GET', 'POST'])
def itemEdit(item_name):
    """ This handler is invoked for editing an item details """
    if login_session['userid']:
        session = DBSession()
        editedItem = session.query(Item).filter_by(name=item_name).one()
        if request.method == 'POST':
            if request.form['name']:
                editedItem.name = request.form['name']
            if request.form['description']:
                editedItem.description = request.form['description']
            if request.form['categories']:
                editedItem.category_id = request.form['categories']
            session.add(editedItem)
            session.commit()

            return redirect(url_for('listCatalog'))
        else:
            return render_template(
                'edit.html', item=editedItem)
    else:
        return render_template(
            'error.html',
            message="You are not authorized to view this page!")


@app.route('/catalog/<string:item_name>/delete',
           methods=['GET', 'POST'])
def itemDelete(item_name):
    """ This handler is invoked for deleting an item """
    if login_session['userid']:
        session = DBSession()
        itemToDelete = session.query(Item).filter_by(name=item_name).all()
        if request.method == 'POST':
            for item in itemToDelete:
                session.delete(item)
            session.commit()

            return redirect(url_for('listCatalog'))
        else:
            return render_template(
                'delete.html', item=item_name)
    else:
        return render_template(
            'error.html',
            message="You are not authorized to view this page!")


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
