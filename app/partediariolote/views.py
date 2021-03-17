from flask_appbuilder import ModelView, BaseView, expose, action, has_access
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.models.sqla.filters import FilterEqualFunction, FilterStartsWith, FilterRelationManyToManyEqual, FilterContains, FilterEqual, FilterInFunction
from app import appbuilder
from wtforms.validators import NumberRange
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
from app.partediariolote.models import Partediariolote
from app.partediarioriego.views import PartediarioriegoView

class PartediarioloteView (ModelView):
    datamodel = SQLAInterface(Partediariolote) 
    related_views=[PartediarioriegoView]
    
    list_columns={'lote','usuario'}

partediariolote_builder = appbuilder.add_view(
    PartediarioloteView,
    "Parte Lote",
)