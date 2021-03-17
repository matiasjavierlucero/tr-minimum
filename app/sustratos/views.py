from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from app import appbuilder
from flask_appbuilder import ModelView,BaseView,expose, action, has_access

from app import db
import random
import string
##########
from app.sustratos.models import Sustrato
from app.unidadmedidas.models import Unidadmedida 
from flask_appbuilder.fields import AJAXSelectField
from flask_appbuilder.fieldwidgets import Select2AJAXWidget, Select2SlaveAJAXWidget, Select2Widget
from flask_appbuilder.models.sqla.interface import SQLAInterface
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms import validators
#### para la descarga + timestamp en nombre del archivo
from flask_appbuilder import ModelView,expose,action
from flask import redirect, send_file
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


class SustratoView(ModelView):
    datamodel = SQLAInterface(Sustrato)
     # estructura -> 'nombreAtributoModel':'nombre_a_Mostrar_en_Columna'
    label_columns = {"nombreSustrato":"Sustrato","descrpcionSustrato":"Descripcion","unidadmedida":"Unidad de Medida"}

    list_columns = ["nombreSustrato","descrpcionSustrato","unidadmedida"] #lista de columnas a mostrar en el listado

    # lista de campos y atributos a mostrar en el "show" de cada registro

    list_title = 'Lista de Sustratos'
    show_title = 'Detalle Sustrato'
    add_title = 'Nuevo Sustrato'
    edit_title = 'Editar Sustrato'

    base_permissions = ['can_list', 'can_show']
    @action("down_excel","Descargar lista","","fa-file-excel-o",single=False)
    def down_excel(self, items):
        output = BytesIO()
        list_items = list()
        excel_columns = SustratoView.list_columns

        for item in items:
            row = dict()
            for col,colname in self.label_columns.items():
                if col in excel_columns:
                    row[colname] = str(getattr(item, col))
                else:
                    pass
            list_items.append(row)

        df = pd.DataFrame(list_items)
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        df.to_excel(writer, 'data', index=False)
        writer.save()
        output.seek(0)

        return send_file(output, attachment_filename='lista_motores' +fecha+ '.xlsx', as_attachment=True)



sustrato_builder = appbuilder.add_view(
    SustratoView,
    "Sustrato",
    icon="fa-balance-scale",
    category="Sustrato",
    category_icon="fa-industry"
)

class mermaView(BaseView):
    @expose('/chartMerma')
    @has_access
    def method3(self):
        url = "/chartMerma"
        return url

   
chart_merma_builder = appbuilder.add_view(
    mermaView,
    "Merma",
    icon='fa-area-chart' ,
    href="/chartMerma", 
    category='Charts' ,
    category_icon="fa-area-chart")