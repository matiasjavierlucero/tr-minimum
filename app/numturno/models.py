from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean
from sqlalchemy.orm import relationship
from app import db

class Numturno (db.Model):
    idNumturno = db.Column(db.Integer, primary_key=True)
    posNumturno = db.Column(db.String(200), nullable=False)
       

    def __repr__(self): 
        return self.posNumturno

        