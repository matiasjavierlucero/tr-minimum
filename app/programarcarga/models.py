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
from app.sustratos.models import Sustrato
from app import db
from datetime import datetime, date
import pytz
tz = pytz.timezone('America/Argentina/Buenos_Aires')



class Programarcarga (db.Model):
    idProgramarcarga = db.Column(db.Integer, primary_key=True)
    fechaProgramarcarga = db.Column(db.Date)
    idUsuarioM = db.Column(db.Integer, db.ForeignKey('ab_user.id'), nullable=False)
    idSustrato = db.Column(db.Integer,db.ForeignKey('sustrato.idSustrato'), nullable=False)
    idPlantaequipo = db.Column(db.Integer, db.ForeignKey('plantaequipo.idPlantaequipo'), nullable=False)
    valorProgramacarga = db.Column(db.Float(),nullable=False)
    fcargaProgramacarga = db.Column(db.Date, default=date.today(), nullable=False)
    idUsuario = db.Column(db.Integer, ForeignKey('ab_user.id'), nullable=False)
    
    def __init__(self,fechaProgramarcarga,idUsuarioM,idSustrato,idPlantaequipo,valorProgramacarga,fcargaProgramacarga,idUsuario):
        self.fechaProgramarcarga=fechaProgramarcarga
        self.idUsuarioM=idUsuarioM
        self.idSustrato=idSustrato
        self.idPlantaequipo=idPlantaequipo
        self.valorProgramacarga=valorProgramacarga
        self.fcargaProgramacarga=fcargaProgramacarga
        self.idUsuario=idUsuario

    def __repr__(self):
        return self.idProgramarcarga
