#### IMPORTS para que funcione el 'created_by' (insertar idUsuario en planta creada)
from flask import g,session
from flask_appbuilder.security.sqla.models import User
from sqlalchemy.ext.declarative import declared_attr
########
from flask_appbuilder import Model
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean, Float
from app.users.models import MyUser
from app.plantas.models import Planta
from app import db
from datetime import datetime, date
import pytz
tz = pytz.timezone('America/Argentina/Buenos_Aires')



class Campania (db.Model):
    idCampania = db.Column(db.Integer, primary_key=True)
    nombreCampania = db.Column(db.String(100), nullable=False)
    idUsuario = db.Column(db.Integer, db.ForeignKey('ab_user.id'), nullable=False)
    idUsuarioM = db.Column(db.Integer, ForeignKey('ab_user.id'), nullable=False)
    fechaCampania = db.Column(db.Date)
    fcreacionCampania = db.Column(db.Date, default=date.today(), nullable=False)
    idPlanta = db.Column(db.Integer, db.ForeignKey('planta.idPlanta'), nullable=False)
    activoCampania=db.Column(db.Boolean,nullable=False)
    
    def __init__(self,nombreCampania,idUsuario,idUsuarioM,fechaCampania,fcreacionCampania,idPlanta,activoCampania):
        self.nombreCampania=nombreCampania
        self.idUsuario=idUsuario
        self.idUsuarioM=idUsuarioM
        self.fechaCampania=fechaCampania
        self.fcreacionCampania=fcreacionCampania
        self.idPlanta=idPlanta
        self.activoCampania=activoCampania



    def __repr__(self):
        return self.idCampania