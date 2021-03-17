#### IMPORTS para que funcione el 'created_by' (insertar idUsuario en planta creada)
from flask import g
from flask_appbuilder.security.sqla.models import User
from sqlalchemy.ext.declarative import declared_attr
########
from flask_appbuilder import Model
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean, Float
from app.plantaequipos.models import Plantaequipo
from app.users.models import MyUser
from app import db
from datetime import datetime, date
import pytz
tz = pytz.timezone('America/Argentina/Buenos_Aires')


class Stsv (Model):
    idStsv = db.Column(db.Integer, primary_key=True)
    fechaStsv = db.Column(db.Date, nullable=False)
    idUsuario = db.Column(db.Integer, db.ForeignKey('ab_user.id'), nullable=False)
    valorstStsv = db.Column(db.Float(10, 0), nullable=False)
    valorsvStsv = db.Column(db.Float(10, 0), nullable=False)
    obsStsv = db.Column(db.String(150), default='No disponible')
    idPlantaequipo = db.Column(db.Integer, db.ForeignKey(
        'plantaequipo.idPlantaequipo'), nullable=False)
    fcargaStsv = db.Column(db.Date, default=date.today(), nullable=False)
    plantaequipo = db.relationship("Plantaequipo")
    idUsuarioM = db.Column(db.Integer, ForeignKey(
        'ab_user.id'), nullable=False)
    Usuario = db.relationship("MyUser", foreign_keys=[idUsuarioM])

    @declared_attr
    def idUsuario(cls):  # declaramos el atributo con el mismo nombre que tiene en el modelo y en la DB
        return Column(
            # hacemos la relacion - el get_user_id, trae el user de la session aparentemente
            Integer, ForeignKey("ab_user.id"), default=cls.get_user_id, nullable=False
        )

    @declared_attr
    def created_by(cls):  # busca la coincidencia de IDs en la tabla de usuario
        return relationship(
            "MyUser",
            primaryjoin="%s.idUsuario == MyUser.id" % cls.__name__,
            enable_typechecks=False,
        )

    def __repr__(self):
        return self.idStsv

    def __init__(self,fechaStsv,idUsuario,valorstStsv,valorsvStsv,obsStsv,idUsuarioM,idPlantaequipo,fcargaStsv):
        self.fechaStsv = fechaStsv
        self.idUsuario=idUsuario
        self.valorstStsv=valorstStsv
        self.valorsvStsv=valorsvStsv    
        self.obsStsv=obsStsv
        self.idUsuarioM=idUsuarioM
        self.idPlantaequipo=idPlantaequipo
        self.fcargaStsv = fcargaStsv
        
    @classmethod  # method para retornar el id del usuaario en session
    def get_user_id(cls):
        try:
            return g.user.id
        except Exception:
            return None

    
