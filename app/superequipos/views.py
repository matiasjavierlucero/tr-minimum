from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.models.sqla.filters import FilterEqualFunction, FilterStartsWith, FilterRelationManyToManyEqual, FilterContains, FilterEqual, FilterInFunction

from app import appbuilder
####################
from app import db
###########
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
from app.superequipos.models import Superequipo
from app.marcas.models import Marca


#Funcion para retornar solo los superequipos activos
def activos():
    activo=True
    return activo



class SuperequipoView(ModelView):
    datamodel = SQLAInterface(Superequipo)
    base_filters = [["activoSuperequipo", FilterEqualFunction, activos],]

    order_columns = ["tipoEquipo.nombreTipoequipo", "marcaEquipo.nombreMarca", "fcargaSuperequipo", "modeloSuperequipo","activoSuperequipo"] #columnas ordenables
    base_order = ("tipoEquipo.nombreTipoequipo","asc") # orden por defecto
    label_columns = {"modeloSuperequipo":"Modelo","fcargaSuperequipo":"Fecha carga",
        "activoSuperequipo":"Estado","marcaEquipo.nombreMarca": "Marca",'marcaEquipo':"Marca equipo", "tipoEquipo":"Tipo de equipo","tipoEquipo.nombreTipoequipo":"Tipo de equipo" ,"Usuario":"Creado por", "planta":"disponible en plantas:"}

    list_columns = {"modeloSuperequipo","marcaEquipo.nombreMarca","tipoEquipo.nombreTipoequipo","activoSuperequipo","fcargaSuperequipo"}

    show_fieldsets =[
        ("Resumen",{"fields":['modeloSuperequipo','tipoEquipo','marcaEquipo','activoSuperequipo', "planta", "Usuario"]})
    ]

    add_fieldsets = [
        ("Información básica",{'fields':['modeloSuperequipo','tipoEquipo','marcaEquipo','activoSuperequipo']})
    ]

    edit_exclude_columns= ['fcargaSuperequipo','created_by',"Usuario","planta"]
    search_columns = ['tipoEquipo', 'marcaEquipo', 'modeloSuperequipo']
    list_title = 'Lista Super-Equipos'
    show_title = 'Detalle super-equipo'
    add_title = 'Nuevo super-equipo'
    edit_title = 'Editar super-equipo'
    base_order = ('tipoEquipo.nombreTipoequipo','asc')

    @action("down_excel","Descargar lista","","fa-file-excel-o",single=False)
    def down_excel(self, items):
        output = BytesIO()
        list_items = list()
        excel_columns = SuperequipoView.list_columns

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

        return send_file(output, attachment_filename='lista_super_equipos' +fecha+ '.xlsx', as_attachment=True)

superequipos_builder = appbuilder.add_view(
    SuperequipoView,
    "Super equipos",
    icon = "fa-folder-open-o",
    category="Equipos",
    category_icon = "fa-wrench"
)
