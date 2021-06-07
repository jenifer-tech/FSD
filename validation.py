from flask import Flask,request,jsonify
app = Flask(__name__)
import re
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base, User

# Connect to Database and create database session
engine = create_engine('sqlite:///fsd.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


def validation(username,mobilenumber,email,gender,subject):
    if not username or not mobilenumber or not email or not gender or not subject:
        return "Please enter all values"
    elif not username.isalpha():
        return "Name allowed only strings"    
    elif not re.match  (r'[^@]+@[^@]+\.[^@]+',email):   
        return "Invalid Email address " 
    elif not  gender.isalpha():
        return "Invalid gender"
    elif not re.search(re.compile(r'(\+91)?(-)?\s*?(91)?\s*?(\d{3})-?\s*?(\d{3})-?\s*?(\d{4})'),mobilenumber):    
        return"Mobile no must contain only 10 numbers"    
  


def getUser(username):
   user = session.query(User).filter_by(username=username).first() 
   user.username=request.form['username']   
   if user:
       return user
   else:
       return None     
    
