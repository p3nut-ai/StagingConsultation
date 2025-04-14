from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event, func
from sqlalchemy.orm import Session

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False) 
    email = db.Column(db.String(100), unique=True, nullable=False)  
    image = db.Column(db.String(200), nullable=False) 
    role = db.Column(db.String(20), nullable=False)  

class FAQS(db.Model):
    __tablename__ = 'FAQS'
    id = db.Column(db.Integer, primary_key=True)
    faq_title = db.Column(db.String(100), nullable=False)
    faq_description = db.Column(db.String(100), nullable=False)




class Consultation(db.Model):
    __tablename__ = 'consultations'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    consultation_type = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.String(10), nullable=False)
    day_of_week = db.Column(db.String(20), nullable=False)
    purpose = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), nullable=True)  
    approved_by = db.Column(db.String(20), db.ForeignKey('users.username'), nullable=True)    
    approved_by_user = db.relationship('User', backref='consultations_approved', lazy=True)

class Availability(db.Model):
    __tablename__ = 'availability'
    
    id = db.Column(db.Integer, primary_key=True)
    availability_id = db.Column(db.Integer, nullable=False, unique=True)
    date = db.Column(db.Date, nullable=False)
    day_of_week = db.Column(db.String(20), nullable=False)  
    start_time = db.Column(db.String(10), nullable=False)  
    end_time = db.Column(db.String(10), nullable=False)  
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  

@event.listens_for(Availability, 'before_insert')
def generate_availability_id(mapper, connection, target):
    session = Session(bind=connection)
    max_id = session.query(func.max(Availability.availability_id)).scalar()
    session.close()
    target.availability_id = (max_id or 0) + 1