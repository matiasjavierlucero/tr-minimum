from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean
from sqlalchemy.orm import relationship
from app import db


class Tdni (Model):
    idTdni = db.Column(db.Integer, primary_key=True)
    tipDni = db.Column(db.String(20), nullable=False)
    
    
    def __repr__(self):
        return self.tipDni