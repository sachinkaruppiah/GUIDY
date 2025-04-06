from flask_sqlalchemy import SQLAlchemy

db= SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    fname = db.Column(db.String(50), nullable = False)
    lname = db.Column(db.String(50), nullable = True)
    email = db.Column(db.String(50), primary_key = True)
    password = db.Column(db.String(50), nullable =False)