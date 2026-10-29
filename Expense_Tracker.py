from flask import Flask,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from datetime import datetime


app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='Expense_detail.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION']=False

db=SQLAlchemy(app)

#==============================================================>
#  MODEL
#=============================================================>

class Expense_Tracker(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(120),unique=True,nullable=False)
    amount=db.Column(db.Float,nullable=False)
    category=db.Column(db.String(120),nullable=False)
    date=db.Column(db.Date,nullale=False)


#=====================================.>
#Validation request Data
#=====================================.>

def Validate_Expense(data,partial):
    if not isinstance(data,dict) or not data:
        return None,({'Error': 'Json required data or in dict'},400)

    allowed_fields={'title','amount','category','date'}
    required_fields=allowed_fields

    if partial:
        if not any(key in data for key in (allowed_fields)):
            return None,({'Error': 'required atleast 1 field'}),400

    elif not required_fields.issubset(data.keys()):
        missing=sorted(required_fields-data.keys())

        return None,({
        'Error': 'Missing required Fields',
        'Fields': missing},400)

    if any(key not in allowed_fields for key in data):
        return None,({'Error': 'Unknown field'},400)

    

    


        




    

