from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Country, CountryItem, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Country Item Application"

# Connect to Database and create database session
engine = create_engine('sqlite:///country.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create anti-forgery state token
@app.route('/login')
def showLogin():

    return render_template('login.html')

#Get a user according to its id
def getUserInfo(user_id):

    user = session.query(User).filter_by(id=user_id).one()
    return user

@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    
    code = request.data
    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        print "oauth_flow === ", oauth_flow
        oauth_flow.redirect_uri = 'postmessage'
        print "oauth_flow.redirect_uri == ", oauth_flow.redirect_uri
        credentials = oauth_flow.step2_exchange(code)
        print "credentials === ", credentials
    except FlowExchangeError:
        print "FlowExchangeError"
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Check that the access token is valid.
    access_token = credentials.access_token
    print "access_token == ", access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    print "result == ", result
    print "result['user_id'] == ", result['user_id']
    print "gplus_id == ", gplus_id
    if result['user_id'] != gplus_id:
        print "FlowExchangeError"
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Verify that the access token is valid for this app.
    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    print "stored_gplus_id  == ", stored_gplus_id
    print "gplus_id == stored_gplus_id:" 
    print "gplus_id ", gplus_id
    print "stored_gplus_id ", stored_gplus_id
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Store the access token in the session for later use.
    login_session['credentials'] = credentials
    login_session['gplus_id'] = gplus_id
    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = answer.json()
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    user_id = getUserID(login_session['email'])
    if (user_id is None):
        print "login doesn't exist ... creating user"
        user_id = createUser(login_session)
    else:
        print "user exists in the DB"
    login_session['user_id'] = user_id
    login_session['provider'] = 'google'
    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    return output 

#Show all countries
@app.route('/')
@app.route('/country/')
def showCountries():

    countries = session.query(Country).order_by(asc(Country.name))
    if 'username' not in login_session:
        return render_template('publiccountries.html', countries=countries)
    else:
        return render_template('countries.html', countries=countries)

#Show a specific country according to its id
@app.route('/country/<int:country_id>/')
def showCountry(country_id):

    country = session.query(Country).filter_by(id=country_id).one()
    print "country.name == ", country.name
    print "country.user_id == ", country.user_id
    creator = getUserInfo(country.user_id)
    print "creator == ", creator.name
    items = session.query(CountryItem).filter_by(
        country_id=country_id).all()
    for item in items:
        print "items == ", item.description
    if 'username' not in login_session:
        return render_template('publiccountry.html', items=items, country=country, creator=creator)
    else:
        return render_template('country.html', items=items, country=country, creator=creator)

#Show a specific country item according to its specific id
@app.route('/country/<int:country_id>/countryitem/<int:countryitem_id>/')
def showCountryItem(country_id, countryitem_id):

    countryItem = session.query(CountryItem).filter_by(id=countryitem_id).one()
    creator = getUserInfo(countryItem.user_id)
    return render_template('publiccountryitem.html', countryItem=countryItem, creator=creator)

#Edit a country item
@app.route('/country/<int:country_id>/item/<int:country_item_id>/edit', methods=['GET','POST'])
def editCountryItem(country_id, country_item_id):

    editedItem = session.query(CountryItem).filter_by(id = country_item_id).one()
    country = session.query(Country).filter_by(id = country_id).one()
    countries = session.query(Country).order_by(asc(Country.name)).filter(Country.name != country.name)
    if request.method == 'POST':
        if request.form['name']:
            editedItem.title = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['country-selection']:
            editedItem.country_id = request.form['country-selection']
        session.add(editedItem)
        session.commit() 
        flash('Country Item Successfully Edited')
        return redirect(url_for('showCountry', country_id = country_id))
    else:
        return render_template('editcountryitem.html', country = country, item = editedItem, countries = countries)

#Delete a country item
@app.route('/country/<int:country_id>/menu/<int:country_item_id>/delete', methods = ['GET','POST'])
def deleteCountryItem(country_id,country_item_id):

    menu_item = session.query(CountryItem).filter_by(id = country_item_id).one()
    creator = getUserInfo(CountryItem.user_id)
    itemToDelete = session.query(CountryItem).filter_by(id = country_item_id).one() 
    if (login_session['user_id'] != creator.id):
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash('Menu Item Successfully Deleted')
        return redirect(url_for('showCountry', country_id = country_id))
    else:
        return render_template('deletecountryitem.html', item = itemToDelete)

#Create a new country item
@app.route('/country/<int:country_id>/item/new/',methods=['GET','POST'])
def newCountryItem(country_id):

  if 'username' not in login_session:
    return redirect('/login')
  country = session.query(Country).filter_by(id = country_id).one()
  countries = session.query(Country).order_by(asc(Country.name)).filter(Country.name != country.name)
  if request.method == 'POST':
      newItem = CountryItem(title = request.form['name'], description = request.form['description'], country_id = request.form['country-selection'])
      session.add(newItem)
      session.commit()
      flash('New Menu %s Item Successfully Created' % (newItem.title))
      return redirect(url_for('showCountry', country_id = country_id))
  else:
      return render_template('newcountryitem.html', country = country, countries = countries)

#User Helper Functions
def createUser(login_session):

    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id

#Get a user according to its id
def getUserInfo(user_id):

    user = session.query(User).filter_by(id=user_id).one()
    return user

#Get a user according to its email
def getUserID(email):

    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

#Disconnect a signed in user
@app.route('/gdisconnect')
def gdisconnect():

    # Only disconnect a connected user.
    credentials = login_session.get('credentials')
    if credentials is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = credentials.access_token
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] != '200':
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

# Disconnect based on provider
@app.route('/disconnect')
def disconnect():

    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['credentials']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('showCountries'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showCountries'))

if __name__ == '__main__':
    app.debug = False
    app.run(host='0.0.0.0', port=5000)