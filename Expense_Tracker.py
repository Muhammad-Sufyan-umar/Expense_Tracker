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


with app.app_context():
    db.create_all()
    

