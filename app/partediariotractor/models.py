from flask import g, Markup, url_for
from flask_appbuilder.security.sqla.models import User
from sqlalchemy.ext.declarative import declared_attr
from flask_appbuilder import Model
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean, Float
from app import db
from datetime import datetime, date
import pytz
tz = pytz.timezone('America/Argentina/Buenos_Aires')

class Partediariotractor (db.Model):
    idPartediariotractor = db.Column(db.Integer, primary_key=True)
    idPlantaequipo = db.Column(db.Integer, db.ForeignKey('plantaequipo.idPlantaequipo'), nullable=False)
    hsPartediariotractor = db.Column(db.Integer, default = 0,nullable=False)
    ltsPartediariotractor = db.Column(db.Integer, default = 0,nullable=False)
    tipoPartedieriotractor=db.Column(db.String(20),nullable=False)
    idPPartedieriotractor = db.Column(db.Integer, db.ForeignKey('partediarioriego.idPartediarioriego'), nullable=False)

    def __repr__(self):
        return self.idPartediariotractor

    def __init__(self,idPartediariotractor,idPlantaequipo,hsPartediariotractor,ltsPartediariotractor,tipoPartedieriotractor):
        self.idPartediariotractor=idPartediariotractor
        self.idPlantaequipo=idPlantaequipo
        self.hsPartediariotractor=hsPartediariotractor
        self.ltsPartediariotractor=ltsPartediariotractor
        self.tipoPartedieriotractor=tipoPartedieriotractor
   