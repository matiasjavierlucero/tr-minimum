from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean,Float
from sqlalchemy.orm import relationship
from app.unidadmedidas.models import Unidadmedida
from app import db

class Sustrato(db.Model):
    idSustrato = db.Column(db.Integer, primary_key=True)
    nombreSustrato = db.Column(db.String(100), nullable=True)
    descrpcionSustrato = db.Column(db.String(100), nullable=True)
    idUnidadmedida = db.Column(db.Integer, ForeignKey("unidadmedida.idUnidadmedida"))
    unidadmedida = db.relationship("Unidadmedida")
    
    def __init__(self,nombreSustrato,descrpcionSustrato,idUnidadmedida,unidadmedida):
        self.nombreSustrato=nombreSustrato
        self.descrpcionSustrato=descrpcionSustrato
        self.idUnidadmedida=idUnidadmedida
        self.unidadmedida=unidadmedida

    def __repr__(self):
        return str(self.nombreSustrato)
