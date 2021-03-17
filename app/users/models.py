from flask_appbuilder.security.sqla.models import User,assoc_user_role # tengo q importar esto para editar el usuario q me crea FAB
from app.roles.models import MyRole
from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean
from sqlalchemy.orm import relationship
from app.paises.models import Pais
from app.tdnis.models import Tdni
from app.plantas.models import Planta
from app.profesiones.models import Profesion
from app import db # esto creo q se import acá, para no renegar con circular imports
from datetime import datetime
import pytz
tz = pytz.timezone('America/Argentina/Buenos_Aires')

class MyUser (User): # atentos acá , al 'user' para que tome el usuario de FAB
    __tablename__ = 'ab_user' # indicamos el nombre de la tabla en la db
    idTdni = db.Column (db.Integer, ForeignKey('tdni.idTdni'), nullable=False)
    idPais = db.Column (Integer, ForeignKey('pais.idPais'), nullable=False)
    idProfesion = db.Column (Integer, ForeignKey('profesion.idProfesion'), nullable=False)
    numerodniUser = db.Column(db.String(50), unique=True ,nullable=False)
    celUser = db.Column(db.String(50), nullable=True)
    fnacimientoUser = db.Column(db.Date,default = datetime.now(tz))
    my_roles = relationship("MyRole", secondary=assoc_user_role, backref="MyUser")

    userPais = relationship('Pais')
    userTdni = relationship('Tdni')
    userProfesion = relationship ('Profesion')

