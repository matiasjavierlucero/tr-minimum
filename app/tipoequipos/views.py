from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from app import appbuilder
####################
from app.tipoequipos.models import Tipoequipo
###########
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


# clase para armar el modelo
class TipoequipoView (ModelView):
    datamodel = SQLAInterface(Tipoequipo) # de donde traemos el modelo, supongo
    label_columns = {"nombreTipoequipo":"Tipo de equipo"} # estructura -> 'nombreAtributoModel':'nombre_a_Mostrar_en_Columna'

    list_columns = ["nombreTipoequipo"] #lista de columnas a mostrar en el listado
    base_order = ("nombreTipoequipo","asc")
    # lista de campos y atributos a mostrar en el "show" de cada registro
    show_fieldsets =[
        ("Resumen",{"fields": ["nombreTipoequipo"]}
        )
        ]
    #campos a mostrar en el CREATE de un nuevo registro
    add_fieldsets = [
        ("Información Básica", {"fields": ["nombreTipoequipo"]})
    ]
    list_title = 'Lista de tipos de equipos'
    show_title = 'Detalle tipo de equipo'
    add_title = 'Nuevo tipo de equipo'
    edit_title = 'Editar tipo de equipo'
    
    
    @action("down_excel","Descargar lista","","fa-file-excel-o",single=False)
    def down_excel(self, items):
        output = BytesIO()
        list_items = list()
        excel_columns = TipoequipoView.list_columns

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

        return send_file(output, attachment_filename='lista_tipo_de_equipos' +fecha+ '.xlsx', as_attachment=True)

# esto es para registrar la vista?
tipoequipos_builder = appbuilder.add_view(
    TipoequipoView,
    "Tipos equipo",
    icon = "fa-folder-open-o",
    category="Equipos",
    category_icon = "fa-wrench"
)
