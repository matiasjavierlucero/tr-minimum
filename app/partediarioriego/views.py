from flask_appbuilder import ModelView, BaseView, expose, action, has_access
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.models.sqla.filters import FilterEqualFunction, FilterStartsWith, FilterRelationManyToManyEqual, FilterContains, FilterEqual, FilterInFunction
from app import appbuilder
from wtforms.validators import NumberRange
from app.stsvs.models import Stsv
from app.plantas.models import Planta
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flask_appbuilder.fieldwidgets import Select2AJAXWidget, Select2SlaveAJAXWidget, Select2Widget
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
from app.partediarioriego.controllers import *
from app.partediarioriego.models import Partediarioriego
###########


def sessionplanta():
    return session['idPlanta']

def redireccionarAddParte():
    return Partediario_riego_add()
def redireccionarShowParte():
    return listado_parte_riego()
def get_planta():
    return str(session['idPlanta'])

class PartediarioriegoView (ModelView):
    datamodel = SQLAInterface(Partediarioriego) # de donde traemos el modelo, supongo
    base_filters = [['idPlanta',FilterEqualFunction, get_planta],]
 
    label_columns={
        "fechaPartediarioriego":"Fecha",
        "obsPartediarioriego":'Observacion',
        "idUsuarioOP":"Operario",
        "usuariocarga":"Cargado por:",
        "fcargaPartediarioriego":"Fecha de Carga :",
        "turnos":"Turno"}
    list_columns={"fechaPartediarioriego","obsPartediarioriego","usuario","usuariocarga","fcargaPartediarioriego","turnos"}
    #list_columns={'Lote','fechaPlanriego','solidoPlanriego','liquidoPlanriego','descrPlanriego'}
    #edit_columns={'nombreCampania','fechaCampania','fcreacionCampania'}
    #
    #show_title="Información de la Campaña"
    #list_title="Listado de Campañas"
    
    add_template= redireccionarAddParte
    base_permissions = ['can_list', 'can_edit']



partediarioriego_builder = appbuilder.add_view(
    PartediarioriegoView,
    "Parte Riego",
)