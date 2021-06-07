from flask import Flask,request,jsonify
app = Flask(__name__)
import re
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base, Forms, User,Forms,FormFields,User_query
from validation import validation


# Connect to Database and create database session
engine = create_engine('sqlite:///fsd.db',connect_args={'check_same_thread': False}, echo=True)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()



# User table 
# This will let us Create a new users and save it in our database
@app.route('/users/', methods=['POST','GET'])
def newUsers_create_get():
    if request.method == 'POST':
        username=request.form['username'] 
        mobilenumber=request.form['mobilenumber']
        email=request.form['email']
        gender=request.form['gender']
        subject=request.form['subject']
        
        error_msg=validation(username,mobilenumber,email,gender,subject)
        if error_msg:
            return jsonify({"message":error_msg}),400  

        existing_user = session.query(User).filter(User.username == username).first()
        if existing_user:
            return  jsonify({"error":"This user already exists in database!"}),400  

        existing_email = session.query(User).filter(User.email == email).first()
        if existing_email:
            return  jsonify({"error":"This Email-Id already exists in database!"}),400 

        newUser = User(username=request.form['username'], 
        mobilenumber=request.form['mobilenumber'],
        email=request.form['email'],
        gender=request.form['gender'],
        subject=request.form['subject'])
        session.add(newUser)
        session.commit()
        return jsonify({"message":"New User added successfully!"}),201
        
    #landing page that will display all the users in our database        
    if request.method == 'GET': 
        return jsonify([
            {
            'id':users.id,
            'username':users.username,
            'mobilenumber':users.mobilenumber,
            'email':users.email,
            'gender':users.gender,
            'subject':users.subject
            } for users in session.query(User).all()
        ]),200    

# This will letget individual users  in our database          
@app.route('/users/<int:id>/',methods=['GET','PUT','DELETE'])
def alter_get_user(id):
    if request.method=="GET":
        fields= session.query(User).filter_by(id=id).one()
        if fields:
            return jsonify(
                {
                    'id'            :   fields.id,
                    'username'      :   fields.username,
                    'mobilenumber'  :   fields.mobilenumber,
                    'email'         :   fields.email,
                    'gender'        :   fields.gender,
                    'subject'       :   fields.subject,                                       
                }
            ),200  
# This will let us Update our users and save it in our database      
    if request.method=="PUT":  
        user = session.query(User).filter_by(id=id).one() 
        user.username=request.form['username']
        user.mobilenumber=request.form['mobilenumber']
        user.email=request.form['email']
        user.gender=request.form['gender']
        user.subject=request.form['subject']
        session.commit()
        return jsonify(
                {
                    'id':user.id,
                    'username':user.username,
                    'mobilenumber':user.mobilenumber,
                    'email':user.email,
                    'gender':user.gender,
                    'subject':user.subject
                } 
            )    

# This will let us Delete our User
    if request.method=="DELETE":
        user = session.query(User).filter_by(id=id).one()
        session.delete(user)
        session.commit()
        return jsonify({'success':'User deleted successfully'}),200
        


# Forms table
# This will let us Create a new forms and save it in our database
@app.route('/forms/', methods=['POST','GET'])
def newForm():
    if request.method == 'POST':
        newForm = Forms(
        form_name=request.form['form_name'] ,
        form_description=request.form['form_description'],
        user_id=request.form['user_id']) 
        session.add(newForm)
        session.commit()
        return jsonify({"message":"New form added successfully!"}),201
#landing page that will display all the forms in our database(list of forms): 
    if request.method=="GET":
        return jsonify([
            {
            'id':form.id,
            'form_name':form.form_name ,
            'form_description':form.form_description, 
            'user_id':form.user_id,                       
            }for form in session.query(Forms).all()
        ]),200        


@app.route('/forms/<int:id>/',methods=['GET','PUT','DELETE'])
def getforms_id(id):
    if request.method=="GET":
        form= session.query(Forms).filter_by(id=id).one()
        if form:
            return jsonify(
                {
                    'id':form.id,
                    'form_name':form.form_name ,
                    'form_description':form.form_description                        
                }
            ),200        
        return jsonify({'error':'Not found'}),404   


    if request.method=="PUT":
        form = session.query(Forms).filter_by(id=id).one() 
        form.form_name=request.form['form_name']
        form.form_description=request.form['form_description']
        session.commit()
        return jsonify(
                {
                    'id':form.id,
                    'form_name':form.form_name,
                    'form_description':form.form_description
                } 
            )    
     
    if request.method=="DELETE":        
        form = session.query(Forms).filter_by(id=id).one()
        session.delete(form)
        session.commit()
        return jsonify({'success':'Form deleted successfully'}),200
        
#Form fields table(Question Table)
@app.route('/formfields/', methods=['POST','GET'])
def newFormfields():
    if request.method == 'POST':
        newForms = FormFields(
        fieldName=request.form['fieldName'] ,
        fieldType=request.form['fieldType'],  
        fieldOptions=request.form['fieldOptions'], 
        fieldPlaceholder=request.form['fieldPlaceholder'], 
        fieldValidation=request.form['fieldValidation'], 
        form_id=request.form['form_id'],)    
        session.add(newForms)
        session.commit()
        return jsonify({"message":"New form fields added successfully!"}),201
#landing page that will display all the fields(form fields) in our database 
    if request.method=="GET":        
        return jsonify([
            {
            'id':formfield.id,
            'fieldName':formfield.fieldName ,
            'fieldType':formfield.fieldType,
            'fieldOptions':formfield.fieldOptions ,
            'fieldPlaceholder':formfield.fieldPlaceholder,
            'fieldValidation':formfield.fieldValidation ,
            }for formfield in session.query(FormFields).all()
        ]),200        
      

@app.route('/formfields/<int:id>/',methods=['GET','PUT','DELETE'])
def getformfields_id(id):
    if request.method=="GET":
        fields= session.query(FormFields).filter_by(id=id).one()
        if fields:
            return jsonify(
                {
                    'id'                :   fields.id,
                    'fieldName'         :   fields.fieldName,
                    'fieldType'         :   fields.fieldType,
                    'fieldOptions'      :   fields.fieldOptions,
                    'fieldPlaceholder'  :   fields.fieldPlaceholder,
                    'fieldValidation'   :   fields.fieldValidation,
                    'form_id'           :   fields.form_id,                      
                }
            ),200        

    if request.method=="PUT":
        form = session.query(FormFields).filter_by(id=id).one() 
        form.fieldName=request.form['fieldName']
        form.fieldType=request.form['fieldType']
        form.fieldOptions=request.form['fieldOptions']
        form.fieldPlaceholder=request.form['fieldPlaceholder']
        form.fieldValidation=request.form['fieldValidation']
        form.form_id=request.form['form_id']
        session.commit()
        return jsonify(
                {
                    'id':form.id,
                    'fieldName':form.fieldName,
                    'fieldType':form.fieldType,
                    'fieldOptions':form.fieldOptions,
                    'fieldPlaceholder':form.fieldPlaceholder,
                    'fieldValidation':form.fieldValidation,
                    'form_id':form.form_id
                } 
            )    

    if request.method=="DELETE":        
        form = session.query(FormFields).filter_by(id=id).one()
        session.delete(form)
        session.commit()
        return jsonify({'success':'Form fields deleted successfully'}),200
        
           
#joining Forms and FormFields Table(get a specific form to fill in) 
@app.route('/form-<id>/',methods=['GET',])
def getformfields(id):
    if request.method=="GET":
        forms = session.query(Forms).join(FormFields,FormFields.form_id==Forms.id).filter_by(form_id=id).all()
        for form in forms:
            form_object = {
                'form_id'           :   form.id,
                'user_id'           :   form.user_id, 
                'form_name'         :   form.form_name ,
                'form_description'  :   form.form_description,
                'form_fields'       :   []
            }
            for fields in form.form_fields:        
                fields = {                
                    'id'                :   fields.id,
                    'fieldName'         :   fields.fieldName,
                    'fieldType'         :   fields.fieldType,
                    'fieldOptions'      :   fields.fieldOptions,
                    'fieldPlaceholder'  :   fields.fieldPlaceholder,
                    'fieldValidation'   :   fields.fieldValidation,
                    'form_id'           :   fields.form_id,                
                }
                form_object['form_fields'].append(fields) 
            return jsonify(form_object) 


#User Query table(Answers Table)
@app.route('/userquery/', methods=['POST','GET'])
def newForms():
    if request.method == 'POST':
        newForms = User_query(
        form_id=request.form['form_id'] ,
        formfields_id=request.form['formfields_id'],  
        user_id=request.form['user_id'], 
        form_value=request.form['form_value'],) 
        session.add(newForms)
        session.commit()
        return jsonify({"message":"New form with answer successfully added!"}),201  

@app.route('/userquery/<int:id>/', methods=['PUT'])
def updateForms(id):
    if request.method=="PUT":
        form = session.query(User_query).filter_by(id=id).one() 
        form.form_id=request.form['form_id']
        form.formfields_id=request.form['formfields_id']
        form.user_id=request.form['user_id']
        form.form_value=request.form['form_value']       
        session.commit()
        return jsonify(
                {
                    'id':form.id,
                    'form_id':form.form_id,
                    'formfields_id':form.formfields_id,
                    'user_id':form.user_id,
                    'form_value':form.form_value,                    
                } 
            ) 
#getting all the  filled form details(View all the filled details):
@app.route('/enquiries/',methods=['GET',])
def getallfilledformdetails():
    if request.method=="GET":
        forms = session.query(Forms).join(FormFields,FormFields.form_id==Forms.id).all()
        userform = session.query(User).join(Forms,Forms.id==User.id).all()
        for form in forms:
            form_object = {
                'form_id'           :   form.id,
                'user_id'           :   form.user_id, 
                'form_name'         :   form.form_name ,
                'form_description'  :   form.form_description,
                'form_fields'       :   []
            }
            for fields in form.form_fields:        
                fields = {                
                    'id'                :   fields.id,
                    'fieldName'         :   fields.fieldName,
                    'fieldType'         :   fields.fieldType,
                    'fieldOptions'      :   fields.fieldOptions,
                    'fieldPlaceholder'  :   fields.fieldPlaceholder,
                    'fieldValidation'   :   fields.fieldValidation,
                    'form_id'           :   fields.form_id,                
                }
            form_object['form_fields'].append(fields)
        for user in userform:
            userform_object = {
                    'id'            :   user.id,
                    'username'      :   user.username,
                    'mobilenumber'  :   user.mobilenumber,
                    'email'         :   user.email,
                    'gender'        :   user.gender,
                    'subject'       :   user.subject,
                    'form'          :   []
            }
            for forms in user.form:        
                formfields = {                
                    'id'                :   forms.id,
                    'form_name'         :   forms.form_name,
                    'form_description'  :   forms.form_description,                                 
                }
        userform_object['form'].append(formfields) 
        return jsonify(form_object,userform_object) 
#getting  the  filled form details(To view the filled details with particular id):
@app.route('/enquiries/<id>/',methods=['GET',])
def getfilledformdetails(id):
    if request.method=="GET":
        forms = session.query(Forms).join(FormFields,FormFields.form_id==Forms.id).filter_by(form_id=id).all()
        userform = session.query(User).join(Forms,Forms.id==User.id).filter_by(user_id=id).all()
        for form in forms:
            form_object = {
                'form_id'           :   form.id,
                'user_id'           :   form.user_id, 
                'form_name'         :   form.form_name ,
                'form_description'  :   form.form_description,
                'form_fields'       :   []
            }
            for fields in form.form_fields:        
                fields = {                
                    'id'                :   fields.id,
                    'fieldName'         :   fields.fieldName,
                    'fieldType'         :   fields.fieldType,
                    'fieldOptions'      :   fields.fieldOptions,
                    'fieldPlaceholder'  :   fields.fieldPlaceholder,
                    'fieldValidation'   :   fields.fieldValidation,
                    'form_id'           :   fields.form_id,                
                }
                form_object['form_fields'].append(fields)
        for user in userform:
            userform_object = {
                    'id'            :   user.id,
                    'username'      :   user.username,
                    'mobilenumber'  :   user.mobilenumber,
                    'email'         :   user.email,
                    'gender'        :   user.gender,
                    'subject'       :   user.subject,
                    'form'          :   []
            }
            for forms in user.form:        
                formfields = {                
                    'id'                :   forms.id,
                    'form_name'         :   forms.form_name,
                    'form_description'  :   forms.form_description,                                 
                }
                userform_object['form'].append(formfields) 
            return jsonify(form_object,userform_object) 




if __name__ == '__main__':   
    app.run(debug = True)