from flask import g,session
from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr
from app.plantas.models import Planta
from app.users.models import MyUser
from app import db

class PlanUsua(MyUser):
    idPlan_usua = Column(db.Integer, primary_key=True )
    idPlanta = db.Column(db.Integer, db.ForeignKey('planta.idPlanta'), nullable=False)
    idUsuario = db.Column(db.Integer, ForeignKey('ab_user.id'), nullable=False,default=MyUser.id)
    usuario = db.relationship('MyUser') #usamos la clase definina en app.users.models
    fcargaPlan_usua = db.Column(Date)
    finicioPlan_usua = db.Column(Date)
    activoPlan_usua = db.Column(db.Boolean())





    ### decoradores para trabajar la idUsuario, que haga el insert del "created_by" (en tabla planta va en idUsuario)
    ### todavía está bajo estudio pero funciona
   

    @declared_attr
    def created_by(cls): # busca la coincidencia de IDs en la tabla de usuario
        return relationship(
            "MyUser",
            primaryjoin="%s.idUsuario == MyUser.id" % cls.__name__,
            enable_typechecks=False,
        )

    def __repr__(self):
        return str(self.idPlan_usua)


    @declared_attr
    def idPlanta(cls):  # declaramos el atributo con el mismo nombre que tiene en el modelo y en la DB
        return Column(
            Integer, ForeignKey("planta.idPlanta"), default=cls.get_planta_id, nullable=False
        )
    

    @classmethod  # method para retornar el id del usuaario en session
    def get_planta_id(cls):
        try:
            print(str(session['idPlanta']))
            return str(session['idPlanta'])
        except Exception:
            return None
