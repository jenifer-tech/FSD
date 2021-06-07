import sys

# for creating the mapper code
from sqlalchemy import Column, ForeignKey, Integer, String

# for configuration and class code
from sqlalchemy.ext.declarative import declarative_base

# for creating foreign key relationship between the tables
from sqlalchemy.orm import relationship

# for configuration
from sqlalchemy import create_engine

# create declarative_base instance
Base = declarative_base()
#Base.query = db_session.query_property()


# we create the class User and extend it from the Base Class.
class User(Base):
    __tablename__ = 'user'

    id          = Column(Integer, primary_key=True)
    username    = Column(String(250),nullable=False)
    mobilenumber=Column(Integer,nullable=False)
    email       = Column(String(250),nullable=False)
    gender      = Column(String(250),nullable=False)
    subject     = Column(String(250),nullable=False)
    form        = relationship('Forms',backref='user', lazy=True)      

class Forms(Base):
    __tablename__ = 'forms'
    id                  =   Column(Integer, primary_key=True)
    form_name           =   Column(String(250),nullable=False)             
    form_description    =   Column(String(250),nullable=False)
    user_id             =   Column(Integer,ForeignKey('user.id'),nullable=False)
    form_fields         =   relationship('FormFields',backref='forms', lazy=True)

     
class FormFields(Base):
    __tablename__='formfields'    
    id                  =   Column(Integer, primary_key=True)
    fieldName           =   Column(String(250),nullable=True) 
    fieldType           =   Column(String(250),nullable=True)
    fieldOptions        =   Column(String(250),nullable=True)
    fieldPlaceholder    =   Column(String(250),nullable=True)
    fieldValidation     =   Column(String(250),nullable=True)
    form_id             =   Column(Integer,ForeignKey('forms.id'),nullable=False)


class User_query(Base):
    __tablename__='userquery' 
    id                  =   Column(Integer, primary_key=True)
    form_id             =   Column(Integer,ForeignKey('forms.id'),nullable=False)
    formfields_id       =   Column(Integer,ForeignKey('formfields.id'),nullable=False) 
    user_id             =   Column(Integer,ForeignKey('user.id'),nullable=False)
    form_value          =   Column(String(250),nullable=True)


engine = create_engine('sqlite:///fsd.db')

Base.metadata.create_all(engine)