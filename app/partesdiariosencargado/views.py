from flask_appbuilder import ModelView,BaseView,expose, action, has_access
from flask_appbuilder.models.sqla.interface import SQLAInterface
from app import appbuilder
from wtforms.validators import Length, NumberRange, AnyOf, NoneOf, Regexp
#### imports charts #####
import random
import string
#### para la descarga + timestamp en nombre del archivo
from flask_appbuilder import ModelView,expose,action
from flask import redirect, send_file
import csv
from io import BytesIO
import pandas as pd
from datetime import datetime
import pytz
from app.partesdiariosencargado.models import Parteencargado
from app.partesdiariosencargado.controllers import *

tz = pytz.timezone('America/Argentina/Buenos_Aires')
fecha = datetime.now(tz)
fecha = fecha.strftime('%Y-%m-%d %H:%M')
fecha = str(fecha)
#############

def redireccionarPartediario():
    return ParteDiarioEncargado

class ParteEncargadoView(ModelView):
    datamodel = SQLAInterface(Parteencargado)
    label_columns = {
                    "plantas":"Planta",
                    "fechaParteencargado":"Fecha de Parte",
                    "obsParteencargado":"Observacion",
                    "usuario":"Operario reportado",
                    "created_by":"Reporte realizado por",
                    "fcargaParteencargado":"Cargado el:",
                    }


    list_columns = ["plantas","fechaParteencargado","obsParteencargado","usuario","created_by","fcargaParteencargado"]  # lista de columnas a mostrar en el listado
    edit_exclude_columns={"plantas","usuariocarga","fcargaParteencargado","created_by"}
    add_exclude_columns={"plantas","usuariocarga","fcargaParteencargado","created_by"}

    add_template=redireccionarPartediario

    list_title = 'Listar Parte Encargado'
    show_title = 'Parte Encargado'
    add_title = 'Agregar Parte Encargado'
    edit_title = 'Editar Parte Encargado'

class ParteEncargadoCargaView(BaseView):
    @expose('/partediarioencargado')
    @has_access
    def chartDigestores(self):
        pass
        return 


parteEncargadoCargaView_builder = appbuilder.add_view(
    ParteEncargadoCargaView,
    "Carga Parte Encargado",
    icon='fa-line-chart',
    href="/partediarioencargado",
    category='Partes',
    category_icon="fa-area-chart"
)

parteEncargadoView_builder = appbuilder.add_view(
    ParteEncargadoView,
    "Listar Partes Encargado",
    icon = "fa-flask",
    category="Partes",
    category_icon = "fa-flask"
)

