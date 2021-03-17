from flask_appbuilder import ModelView,BaseView,expose, action, has_access
from flask_appbuilder.models.sqla.interface import SQLAInterface
from app import appbuilder
from wtforms.validators import Length, NumberRange, AnyOf, NoneOf, Regexp
from flask_appbuilder.models.sqla.filters import FilterEqualFunction, FilterStartsWith, FilterRelationManyToManyEqual, FilterContains, FilterEqual, FilterInFunction

#### imports charts #####
import random
import string
#### para la descarga + timestamp en nombre del archivo
from flask_appbuilder import ModelView,expose,action
from flask import redirect, send_file,session
import csv
from io import BytesIO
import pandas as pd
from datetime import datetime
import pytz
from app.parteoperario.models import Parteoperario
from app.parteoperario.controllers import *

###########

def querysplanta():
    idPlanta=str(session['idPlanta'])
    return idPlanta

def redireccionarEditar():
    return editarPartesPlanta()

def redireccionarAgregar():
    return cargarParteOperario()

# clase para armar el modelo
class ParteOperarioView (ModelView):
    datamodel = SQLAInterface(Parteoperario) # de donde traemos el modelo, supongo
    base_filters = [["idPlanta", FilterInFunction, querysplanta],]
    label_columns = {"plantas":"Planta","Usuario":"Operario reportado","fechaParteoperario":"Fecha de Parte","turno":"Turno","obsParteoperario":"Observaciones"}

    add_columns= None
    add_exclude_columns=["plantas","Usuario","fechaParteoperario","turno","obsParteoperario","plantas","created_by","fcargaParteoperario"]
    list_columns = {"plantas":"Planta","Usuario":"Usuario reportado","fechaParteoperario":"Fecha de Parte","turno":"Turno","obsParteoperario":"Observaciones"}
   
    list_title = 'Reportes Operarios'
    show_title = 'Reporte de Operario'
    edit_title = 'Editar Reporte'

    edit_exclude_columns= ["plantas","created_by","fcargaParteoperario"]
    edit_template= redireccionarEditar
    add_template= redireccionarAgregar
    

parteoperario_builder = appbuilder.add_view(
    ParteOperarioView,
    "Listar Partes Operario",
    icon="fa-industry",
    category="Partes",
    category_icon="fa-industry"
)

class CargaParteOperarioView(BaseView):
    @expose('/cargarparteoperario')
    @has_access
    def cargarParteOperario(self):
        pass
        return 


cargarparteoperario_builder = appbuilder.add_view(
    CargaParteOperarioView,
    "Cargar Partes Operario",
    icon='fa-line-chart',
    href="/cargarparteoperario",
    category='Partes',
    category_icon="fa-area-chart"
)


class GuardarEdicionPartesPlantaView(BaseView):
    @expose('/guardarCambiosParteOperario/<id>')
    @has_access
    def guardaredicionpartesPlanta(self):
        pass
        return 

