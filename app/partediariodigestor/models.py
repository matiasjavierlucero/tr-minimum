from flask import g, Markup, url_for
from flask_appbuilder.security.sqla.models import User
from sqlalchemy.ext.declarative import declared_attr
from flask_appbuilder import Model
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean, Float
from app.users.models import MyUser
from app.parteoperario.models import Parteoperario
from app.plantaequipos.models import Plantaequipo
from app import db
from datetime import datetime, date
import pytz
tz = pytz.timezone('America/Argentina/Buenos_Aires')

class Partediariodigestor (db.Model):
    idPartediariodigestor = db.Column(db.Integer, primary_key=True)
    idPlantaequipo = db.Column(db.Integer, db.ForeignKey('plantaequipo.idPlantaequipo'), nullable=False)
    costraPartediariodigestor = db.Column(db.Boolean(),nullable=False)
    espumaPartediariodigestor = db.Column(db.Boolean(),nullable=False)
    idParteopeario = db.Column(db.Integer, db.ForeignKey('parteoperario.idParteoperario'), nullable=False)
    def __repr__(self):
        return self.idPartediariodigestor

    def __init__(self,idPlantaequipo,costraPartediariodigestor,espumaPartediariodigestor,idParteopeario):

        self.idPlantaequipo=idPlantaequipo
        self.costraPartediariodigestor=costraPartediariodigestor
        self.espumaPartediariodigestor=espumaPartediariodigestor
        self.idParteopeario=idParteopeario
        
   