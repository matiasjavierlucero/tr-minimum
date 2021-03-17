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
from app.campanias.models import Campania ####### import del MODEL de pais
from app.campanias.controllers import *
###########

def sessionplanta():
    return session['idPlanta']

def redireccionarAgregarCampania():
    return nuevacampania()

def redireccionarShowCampania():
    return infocampania()

def get_planta():
    return str(session['idPlanta'])


# clase para armar el modelo
class CampaniaView (ModelView):
    datamodel = SQLAInterface(Campania) # de donde traemos el modelo, supongo
    base_filters = [['idPlanta',FilterEqualFunction, get_planta],]
    

    label_columns={'nombreCampania':'Nombre',
    "fechaCampania":"Inicio",
    "fcreacionCampania":"Cargada el :",
    "activoCampania":"Activo/Inactivo"}
    list_columns={'nombreCampania','fechaCampania','fcreacionCampania','activoCampania'}
    edit_columns={'nombreCampania','fechaCampania','fcreacionCampania'}
    
    show_title="Información de la Campaña"
    list_title="Listado de Campañas"
    
    add_template= redireccionarAgregarCampania

    show_template=redireccionarShowCampania
    
    base_filters = [['idPlanta', FilterEqualFunction, sessionplanta]]

camp_builder = appbuilder.add_view(
    CampaniaView,
    "Camp",
)

# clase para armar el modelo
class NuevaCampaniaView(BaseView):
    @expose('/nuevacampania')
    @has_access
    def chartDigestores(self):
        pass
        return 


campania_builder = appbuilder.add_view(
    NuevaCampaniaView,
    "FosTac Carga Masiva",
    icon='fa-line-chart',
    href="/nuevacampania",
    category='Campañas',
    category_icon="fa-area-chart"
)