from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from app import appbuilder
from app.areas.models import Area
#from app.plantas.views import PlantaView
#### para la descarga + timestamp en nombre del archivo
from flask_appbuilder import ModelView,expose,action
from flask import redirect, send_file
import csv
from io import BytesIO
import pandas as pd
from datetime import datetime
import pytz
from app.incrementocampania.models import Incremcampania
tz = pytz.timezone('America/Argentina/Buenos_Aires')
fecha = datetime.now(tz)
fecha = fecha.strftime('%Y-%m-%d %H:%M')
fecha = str(fecha)
#############

class IncremcampaniaView(ModelView):
    datamodel=SQLAInterface(Incremcampania)

# esto es para registrar la vista?
incremento_builder = appbuilder.add_view_no_menu(
    IncrementoCampaña
)
