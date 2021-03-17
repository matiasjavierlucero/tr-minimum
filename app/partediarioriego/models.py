from flask import g, Markup, url_for
from flask_appbuilder.security.sqla.models import User
from sqlalchemy.ext.declarative import declared_attr
from flask_appbuilder import Model
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean, Float
from app.users.models import MyUser
from app.plantas.models import Planta
from app.numturno.models import Numturno
from app import db
from datetime import datetime, date
import pytz
tz = pytz.timezone('America/Argentina/Buenos_Aires')

class Partediarioriego (db.Model):
    idPartediarioriego = db.Column(db.Integer, primary_key=True)
    idPlanta = db.Column(db.Integer, db.ForeignKey('planta.idPlanta'), nullable=False)
    fechaPartediarioriego = db.Column(db.Date, default = date.today(),nullable=False)
    obsPartediarioriego=db.Column(db.String(255))
    idUsuarioOP = db.Column(db.Integer, ForeignKey('ab_user.id'), nullable=False)
    idUsuario   = db.Column(db.Integer, ForeignKey('ab_user.id'), nullable=False)
    fcargaPartediarioriego = db.Column(db.Date, default = datetime.now(tz),nullable=False)
    idNumturno=db.Column(db.Integer,ForeignKey('numturno'),nullable=False)
    usuario = db.relationship('MyUser', foreign_keys=[idUsuarioOP])
    usuariocarga = db.relationship('MyUser', foreign_keys=[idUsuario])
    plantas = db.relationship("Planta")
    turnos = db.relationship("Numturno")
    
    
    def __repr__(self):
        return str(self.idPartediarioriego)

    def __init__(self,idPlanta,fechaPartediarioriego,obsPartediarioriego,idUsuarioOP,idUsuario,fcargaPartediarioriego,idNumturno):
        self.idPlanta=idPlanta
        self.fechaPartediarioriego=fechaPartediarioriego
        self.obsPartediarioriego=obsPartediarioriego
        self.idUsuarioOP=idUsuarioOP
        self.idUsuario=idUsuario
        self.fcargaPartediarioriego=fcargaPartediarioriego
        self.idNumturno=idNumturno

   