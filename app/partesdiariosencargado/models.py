from flask import g, Markup, url_for
from flask_appbuilder.security.sqla.models import User
from sqlalchemy.ext.declarative import declared_attr
from flask_appbuilder import Model
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean, Float
from app.users.models import MyUser
from app.plantas.models import Planta
from app import db
from datetime import datetime, date
import pytz
tz = pytz.timezone('America/Argentina/Buenos_Aires')

class Parteencargado (db.Model):
    idParteencargado = db.Column(db.Integer, primary_key=True)
    idPlanta = db.Column(db.Integer, db.ForeignKey('planta.idPlanta'), nullable=False)
    fechaParteencargado = db.Column(db.Date, default = date.today(),nullable=False)
    obsParteencargado=db.Column(db.String(255))
    idUsuarioOP = db.Column(db.Integer, ForeignKey('ab_user.id'), nullable=False)
    idUsuario = db.Column(db.Integer, ForeignKey('ab_user.id'), nullable=False)
    fcargaParteencargado = db.Column(db.Date, default = datetime.now(tz),nullable=False)
    usuario = db.relationship('MyUser', foreign_keys=[idUsuarioOP])
    plantas = db.relationship("Planta")
    
    def __repr__(self):
        return self.idParteencargado

    def __init__(self,idPlanta,fechaParteencargado,obsParteencargado,idUsuarioOP,idUsuario,fcargaParteencargado):
        self.idPlanta=idPlanta
        self.fechaParteencargado=fechaParteencargado
        self.obsParteencargado=obsParteencargado
        self.idUsuarioOP=idUsuarioOP
        self.idUsuario=idUsuario
        self.fcargaParteencargado=fcargaParteencargado
   
    @declared_attr
    def idUsuario(cls):  # declaramos el atributo con el mismo nombre que tiene en el modelo y en la DB
        return Column(
            # hacemos la relacion - el get_user_id, trae el user de la session aparentemente
            Integer, ForeignKey("ab_user.id"), default=cls.get_user_id, nullable=False
        )

    #@declared_attr
    #def idPlanta(cls):  # declaramos el atributo con el mismo nombre que tiene en el modelo y en la DB
    #    return Column(
    #        Integer, ForeignKey("planta.idPlanta"), default=cls.get_planta_id, nullable=False
    #    )

    @declared_attr
    def created_by(cls):  # busca la coincidencia de IDs en la tabla de usuario
        return relationship(
            "MyUser",
            primaryjoin="%s.idUsuario == MyUser.id" % cls.__name__,
            enable_typechecks=False,
        )


    @classmethod  # method para retornar el id del usuaario en session
    def get_user_id(cls):
        try:
            return g.user.id
        except Exception:
            return None

    #@classmethod  # method para retornar el id del usuaario en session
    #def get_planta_id(cls):
    #    try:
    #        print(str(session['idPlanta']))
    #        return str(session['idPlanta'])
    #    except Exception:
    #        return None
