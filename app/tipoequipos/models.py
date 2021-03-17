from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean
from sqlalchemy.orm import relationship
from app import db

class Tipoequipo (db.Model):
    idTipoequipo = db.Column(db.Integer, primary_key=True)
    nombreTipoequipo = db.Column(db.String(100), nullable=False)
    
    def __init__(self,nombreTipoequipo):
        self.nombreTipoequipo=nombreTipoequipo
       
    
    def __repr__(self): 
        return self.nombreTipoequipo