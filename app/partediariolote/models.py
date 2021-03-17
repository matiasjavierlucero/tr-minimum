from flask import g, Markup, url_for
from flask_appbuilder.security.sqla.models import User
from sqlalchemy.ext.declarative import declared_attr
from flask_appbuilder import Model
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean, Float
from app import db
from datetime import datetime, date
import pytz
tz = pytz.timezone('America/Argentina/Buenos_Aires')

from app.partediarioriego.models import Partediarioriego
from app.lotes.models import Lote

class Partediariolote (db.Model):
    idPartediarioLote = db.Column(db.Integer, primary_key=True)
    idLote = db.Column(db.Integer, db.ForeignKey('lote.idLote'), nullable=False)
    solidoPartediariolote = db.Column(db.Float(10,2),default=0)
    liquidoPartediariolote = db.Column(db.Float(10,2),default=0)
    idPartediarioriego = db.Column(db.Integer, ForeignKey('partediarioriego.idPartediarioriego'), nullable=False)
    parteriego= db.relationship("Partediarioriego")
    lote=db.relationship("Lote")
    
    def __repr__(self):
        return str(self.idPartediarioLote)

    def __init__(self,idLote,solidoPartediariolote,liquidoPartediariolote,idPartediarioriego):
        self.idLote=idLote
        self.solidoPartediariolote=solidoPartediariolote
        self.liquidoPartediariolote=liquidoPartediariolote
        self.idPartediarioriego=idPartediarioriego
  
