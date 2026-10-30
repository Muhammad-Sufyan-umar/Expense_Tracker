from flask import Flask,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from datetime import datetime


app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///Expense_detail.db'
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
    date=db.Column(db.Date,nullable=False)

#=====================================.>
#Validation request Data
#=====================================.>

def Validate_Expense(data,partial=False):
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

    

    cleaned={}

    #Validate Title
    if 'title' in data:
        if not isinstance(data['title'],str):
            return None,({'Error':'title must be in Text Form'},400)
        title=data['title'].strip()
        if not title:
            return None,({'Error': 'Title Must required'},400)
        
        cleaned['title'] = title


    #Validate Amount
    if 'amount' in data:
        amount=data['amount']
        if isinstance(amount,bool) or not isinstance(amount,(int,float)):
            return None,({'Error': 'Amount must e Int or Float'},400)

        if amount<=0:
            return None,({'Error':'Must be Greater than zero'},400)

        cleaned['amount']=amount

    #Validate category
    
    if 'category' in data:
        if not isinstance(data['category'],str):
            return None,({'Error': 'Category Must be In Text'},400)
        category=data['category'].strip()
        if not category:
            return None,({'Error': 'Must be required Category'},400)
        cleaned['category']=category


    #Validate Date
    if 'date' in data:
        date_string=data['date']

        if not isinstance(date_string,str) or not date_string:
            return None,({'Error': 'Date is required as YYYY-MM-DD'},400)
        try:
            cleaned['date']=datetime.strptime(
                date_string,'%Y-%m-%d'
            ).date()

        except ValueError:
            return None,({
                'Error': 'Invalid date-- Use YYYY-MM-DD format'
            },400)

        return cleaned,None


#==============================================================>
#Create Expense
#==============================================================>

@app.route('/expense',methods=['POST'])
def create_expenses():
    data=request.get_json(silent=True)

    cleaned,error=Validate_Expense(data)

    if error:
        return error
    new_expense=Expense_Tracker(**cleaned)
    db.session.add(new_expense)

    try:
        db.session.commit()
        return {'ID': new_expense.id},201
    except IntegrityError:
        db.session.rollback()
        return {'Error': 'Data with this title already exists'},409

#=========================================================>
#GET ALL
#===========================================================>

@app.route('/expense',methods=['GET'])
def Get_All():
    category=request.args.get('category')
    
    all_data=Expense_Tracker.query.all()
    
    if category:
        all_data=Expense_Tracker.query.filter_by(category=category).all() 
    
    output=[
    
        {
            'ID':data.id,
            'Title':data.title,
            'Amount':data.amount,
            'Category': data.category,
            'Date': data.date.isoformat()
        }
        for data in all_data
        ]


    return {'Json': output},200

#==========================================================>
#GET BY ID
#==========================================================>

@app.route('/expense/<int:id>',methods=['GET'])
def Get_By_Id(id):
    expense=db.get_or_404(Expense_Tracker,id)

    return {
        'id':expense.id,
        'title':expense.title,
        'amount':expense.amount,
        'category':expense.category,
        'date':expense.date.isoformat()
    },200


#==========================================================>
#PATACH
#========================================================>

@app.route('/expense/<int:id>',methods=['PATCH'])

def Update_Expense(id):
    expense=db.get_or_404(Expense_Tracker,id)
    data=request.get_json(silent=True)

    cleaned,error=Validate_Expense(data,partial=True)

    if error:
        return error

    #Validate Everything Before Updating
    for fields,value in cleaned.items():
        setattr(expense,fields,value)

    try:
        db.session.commit()
        return {
            'Message': 'Expense Updated Successfully',
            'ID': expense.id,
            'Title': expense.title,
            'Amount': expense.amount,
            'Category': expense.category,
            'Date': expense.date.isoformat()
        },200
    except IntegrityError:
        db.session.rollback()
        return {'Error': 'Data with this title already exists'},409

#==========================================================>
#DELETE
#==========================================================>

@app.route('/expense/<int:id>',methods=['DELETE'])
def Delete_Expense(id):
    expense=db.get_or_404(Expense_Tracker,id)

    db.session.delete(expense)
    db.session.commit()

    return {'Message': 'expense deleted Successfully'},200