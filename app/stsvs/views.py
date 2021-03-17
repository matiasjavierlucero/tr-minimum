from flask_appbuilder import ModelView,BaseView,expose, action, has_access
from flask_appbuilder.models.sqla.interface import SQLAInterface
from app import appbuilder
from wtforms.validators import NumberRange
from app.stsvs.models import Stsv
from app.stsvs.controllers import stsvcargamasiva
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
tz = pytz.timezone('America/Argentina/Buenos_Aires')
fecha = datetime.now(tz)
fecha = fecha.strftime('%Y-%m-%d %H:%M')
fecha = str(fecha)
#############
#############



def redireccionarCargamasivastsv():
    return stsvcargamasiva()

class StsvView(ModelView):
    datamodel = SQLAInterface(Stsv)

    label_columns = {"fechaStsv":"Fecha","valorstStsv":"Valor St (%)", "valorsvStsv":"Valor Sv (%)",
                     "plantaequipo":"Planta", "Usuario":"Medido por:", "obsStsv":"Observaciones"}

    list_columns = ["plantaequipo","valorstStsv","valorsvStsv","tacobsStsvFostac","Usuario"]
    
    add_exclude_columns = ['created_by', 'fcargaStsv']
    edit_exclude_columns = ['created_by', 'fcargaStsv']
    list_exclude_columns = ['created_by', 'fcargaStsv']


    list_title = 'Lista de registros Stsv'
    show_title = 'Detalle Stsv'
    add_title = 'Nuevo registro Stsv '
    edit_title = 'Editar registro Stsv'

    add_template=redireccionarCargamasivastsv
 
    @action("down_excel","Descargar lista","","fa-file-excel-o",single=False)
    def down_excel(self, items):
        output = BytesIO()
        list_items = list()
        excel_columns = StsvView.list_columns

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

        return send_file(output, attachment_filename='Stsv' +fecha+ '.xlsx', as_attachment=True)


stsv_builder = appbuilder.add_view(
    StsvView,
    "Stsv",
    icon="fa-industry",
    category="Área/Planta",
    category_icon="fa-industry"
)

class CargaMasivastsvView(BaseView):
    @expose('/stsv')
    @has_access
    def chartDigestores(self):
        pass
        return 



stsvmasiva_builder = appbuilder.add_view(
    CargaMasivastsvView,
    "stsvCargaMasiva",
    icon='fa-line-chart',
    href="/cargamasivastsv",
    category='stsv',
    category_icon="fa-area-chart"
)