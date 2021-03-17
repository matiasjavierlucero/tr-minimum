import logging ## import de logging
from flask import g
from flask_appbuilder.security.sqla.models import User
from flask_appbuilder.security.sqla.models import Role
from sqlalchemy.ext.declarative import declared_attr
#### imports de flasks
from flask import Flask
from flask_appbuilder import SQLA, AppBuilder
from flask_appbuilder.menu import Menu
from app.index import MyIndexView

###Import de los templates personalizados
from flask import Flask, render_template, request, redirect, url_for, flash, session, make_response,Response
#from flask_mysqldb import MySQL
import os
from os import environ 
import pytz
from datetime import datetime

### LOGGING CONFIG ###############
#logging.basicConfig(format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
#logging.getLogger().setLevel(logging.DEBUG)

######## "ARMAMOS" LA APP #####################
app = Flask(__name__)
#Logging
# logging.basicConfig(filename='debug.log',
# level=logging.DEBUG,
# format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

# logging.basicConfig(filename='info.log',
# level=logging.INFO,
# format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

# logging.basicConfig(filename='error.log',
# level=logging.ERROR,
# format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

# logging.basicConfig(filename='warning.log',
# level=logging.WARNING,
# format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

app.config.from_object("config")
db = SQLA(app)


######### tengo que respetar el orden del import ,para evitar circular de app y db gralmente. (está bajo estudio)
from app.users.sec import MySecurityManager
appbuilder = AppBuilder(app, db.session,indexview=MyIndexView, menu=Menu(reverse=False), security_manager_class=MySecurityManager, base_template='my_index.html')


######### importamos todas las views ############# debe hacerse al final para evitar circular import
from . import all_views

#Importo los modelos necesarios para el controller
from app.fostac.controllers import *
from app.plantas.controllers import *
from app.chartScada.controllers import *
from app.sustratos.controllers import *
from app.motores.controllers import *
from app.stsvs.controllers import *
from app.partesdiariosencargado.controllers import *
from app.parteoperario.controllers import * 
from app.users.controllers import *
from app.campanias.controllers import *
from app.programarcarga.controllers import *
from app.tipoequipos.controllers import *
from app.plantaequipos.controllers import *
from app.superequipos.controllers import *
from app.planriego.controllers import *
from app.incascada.controller import *
from app.partediarioriego.controllers import *