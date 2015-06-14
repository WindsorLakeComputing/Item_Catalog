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

# Connect to Database and create database session
engine = create_engine('sqlite:///country.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create anti-forgery state token
@app.route('/login')
def showLogin():
    return render_template('login.html')

def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


# Show all countries
@app.route('/')
@app.route('/country/')
def showCountries():
    countries = session.query(Country).order_by(asc(Country.name))
    if 'username' not in login_session:
        return render_template('publiccountries.html', countries=countries)
    else:
        return render_template('publiccountries.html', countries=countries)


@app.route('/country/<int:country_id>/')
#@app.route('/restaurant/<int:restaurant_id>/menu/')
def showCountry(country_id):
    country = session.query(Country).filter_by(id=country_id).one()
    print "country.name == ", country.name
    print "country.user_id == ", country.user_id
    creator = getUserInfo(country.user_id)
    print "creator == ", creator.name
    items = session.query(CountryItem).filter_by(
        country_id=country_id).all()
    #if 'username' not in login_session or creator.id != login_session['user_id']:
    #    return render_template('publicmenu.html', items=items, restaurant=restaurant, creator=creator)
    #else:
    #    return render_template('menu.html', items=items, restaurant=restaurant, creator=creator)


if __name__ == '__main__':
    #app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)