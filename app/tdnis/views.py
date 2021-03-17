from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from app import appbuilder
####################
from app.tdnis.models import Tdni ####### import del MODEL de provincia
#from app.paises.views import PaisView  ############### tener cuidado con esto ESTUDIAR
###########



# clase para armar el modelo
class TdniView (ModelView):
    datamodel = SQLAInterface(Tdni) 
    #related_views = [PaisView]  ############### tener cuidado con esto
    label_columns = {"tipDni":"Tipo de DNI"} # estructura -> 'nombreAtributoModel':'nombre_a_Mostrar_en_Columna'

    list_columns = ["tipDni"] #lista de columnas a mostrar en el listado

    # lista de campos y atributos a mostrar en el "show" de cada registro
    #show_fieldsets =[('Resumen',{'fields': ['nomProvincia', 'paisProvincia']})]

    #campos a mostrar en el CREATE de un nuevo registro
    add_fieldsets = [
        ("Información Básica", {"fields": ["tipDni"]})
    ]

# esto es para registrar la vista?
tdnis_builder = appbuilder.add_view_no_menu(
    TdniView,
    "Tipo dni",
)
