#### IMPORTS para que funcione el 'created_by' (insertar idUsuario en planta creada)
from flask import g 
from flask_appbuilder.security.sqla.models import User
from sqlalchemy.ext.declarative import declared_attr
########
from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean
from sqlalchemy.orm import relationship
#from app.provincias.models import Provincia
from app.tipoequipos.models import Tipoequipo
from app.marcas.models import Marca
from app import db
from datetime import datetime
import pytz
tz = pytz.timezone('America/Argentina/Buenos_Aires')

class Superequipo(Model):
    idSuperequipo = db.Column(db.Integer, primary_key=True)
    idTipoequipo = db.Column(db.Integer,ForeignKey('tipoequipo.idTipoequipo'),nullable=False)
    idMarca = db.Column(db.Integer,ForeignKey('marca.idMarca'),nullable=False,default=1)
    idUsuario = db.Column(db.Integer,ForeignKey('ab_user.id'),nullable=False)
    modeloSuperequipo = db.Column(db.String(150), default='No disponible')
    fcargaSuperequipo = db.Column(Date, default=datetime.now(tz))
    activoSuperequipo = db.Column(db.Boolean(), default=1)
    tipoEquipo =  db.relationship ('Tipoequipo')
    marcaEquipo =  db.relationship ('Marca')
    Usuario = db.relationship('MyUser')


    ### decoradores para trabajar la idUsuario, que haga el insert del "created_by" (en tabla planta va en idUsuario)
    ### todavía está bajo estudio pero funciona
    @declared_attr
    def idUsuario(cls): # declaramos el atributo con el mismo nombre que tiene en el modelo y en la DB
        return Column(
            Integer, ForeignKey("ab_user.id"), default=cls.get_user_id, nullable=False ## hacemos la relacion - el get_user_id, trae el user de la session aparentemente
        )

    @declared_attr
    def created_by(cls): # busca la coincidencia de IDs en la tabla de usuario
        return relationship(
            "MyUser",
            primaryjoin="%s.idUsuario == MyUser.id" % cls.__name__,
            enable_typechecks=False,
        )


    @classmethod ## method para retornar el id del usuaario en session
    def get_user_id(cls):
        try:
            return g.user.id
        except Exception:
            return None

    def __repr__(self):
        return self.modeloSuperequipo