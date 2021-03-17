#### IMPORTS para que funcione el 'created_by' (insertar idUsuario en planta creada)
from flask import g,session
from flask_appbuilder.security.sqla.models import User
from sqlalchemy.ext.declarative import declared_attr
########
from flask_appbuilder import Model
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean, Float
from app.users.models import MyUser
from app import db
from datetime import datetime, date
import pytz
tz = pytz.timezone('America/Argentina/Buenos_Aires')



class Incremcampania (db.Model):
    idIncremcampania = db.Column(db.Integer, primary_key=True)
    idCampania = db.Column(db.Integer, db.ForeignKey('campania.idCampania'), nullable=False)
    idUsuarioM = db.Column(db.Integer, ForeignKey('ab_user.id'), nullable=False)
    fechaIncremcampania = db.Column(db.Date)
    tipoIncremcampania= db.Column(db.Boolean)
    restanteIncremcampania=db.Column(db.Integer)
    idSustrato=db.Column(db.Integer, db.ForeignKey('sustrato.idSustrato'), nullable=False)
    incrementoIncremcampania=db.Column(db.Integer)
    valorIncremcampania=db.Column(db.Float())
    cargatecnicaIncremcampania=db.Column(db.Integer())
    idUsuario = db.Column(db.Integer, db.ForeignKey('ab_user.id'), nullable=False)
    fcargaIncremcampania = db.Column(db.Date, default = datetime.now(tz),nullable=False)


    def __init__(self,idCampania,idUsuarioM,fechaIncremcampania,tipoIncremcampania,restanteIncremcampania,idSustrato,incrementoIncremcampania,valorIncremcampania,cargatecnicaIncremcampania,idUsuario,fechacargaIncremcampania):
        self.idCampania=idCampania
        self.idUsuarioM=idUsuarioM
        self.fechaIncremcampania=fechaIncremcampania
        self.tipoIncremcampania=tipoIncremcampania
        self.restanteIncremcampania=restanteIncremcampania
        self.idSustrato=idSustrato
        self.incrementoIncremcampania=incrementoIncremcampania
        self.valorIncremcampania=valorIncremcampania
        self.cargatecnicaIncremcampania=cargatecnicaIncremcampania
        self.idUsuario=idUsuario
        self.fechacargaIncremcampania=fechacargaIncremcampania


    def __repr__(self):
        return self.idIncremcampania

    @declared_attr
    def idUsuario(cls):  # declaramos el atributo con el mismo nombre que tiene en el modelo y en la DB
        return Column(
            # hacemos la relacion - el get_user_id, trae el user de la session aparentemente
            Integer, ForeignKey("ab_user.id"), default=cls.get_user_id, nullable=False
        )

    @classmethod  # method para retornar el id del usuaario en session
    def get_user_id(cls):
        try:
            return g.user.id
        except Exception:
            return None

   
