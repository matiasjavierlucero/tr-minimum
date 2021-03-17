from flask_appbuilder import ModelView, BaseView, expose, action, has_access
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.models.sqla.filters import FilterEqualFunction, FilterStartsWith, FilterRelationManyToManyEqual, FilterContains, FilterEqual, FilterInFunction
from app import appbuilder
from wtforms.validators import NumberRange
from app.stsvs.models import Stsv
#### imports charts #####
import random
import string
#### para la descarga + timestamp en nombre del archivo
from flask_appbuilder import ModelView, expose, action
from flask import redirect, send_file,session
import csv
from io import BytesIO
import pandas as pd
from datetime import datetime
import pytz
tz = pytz.timezone('America/Argentina/Buenos_Aires')
fecha = datetime.now(tz)
fecha = fecha.strftime('%Y-%m-%d %H:%M')
fecha = str(fecha)
#############
from app.programarcarga.models import Programarcarga ####### import del MODEL de pais
from app.programarcarga.controllers import ProgramarCarga
###########

def redireccionarProgramarCarga():
    return ProgramarCarga()

class ProgramarcargaView (ModelView):
    datamodel = SQLAInterface(Programarcarga) # de donde traemos el modelo, supongo
    

    add_template:redireccionarProgramarCarga

programarcarga_builder = appbuilder.add_view(
    ProgramarcargaView,
    "Programar Carga",
    
)


