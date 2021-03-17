from flask_babelpkg import lazy_gettext as _
from flask_appbuilder.security.views import UserDBModelView
from wtforms.validators import Length, NumberRange, AnyOf, NoneOf, Regexp
#from users.models import MyUser

# para aplicar filtro por defecto 

from flask_appbuilder.models.sqla.filters import FilterEqualFunction,FilterStartsWith
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

class MyUserDBModelView(UserDBModelView):
    """
        View that add DB specifics to User view.
        Override to implement your own custom view.
        Then override userdbmodelview property on SecurityManager
    """

    label_columns = {'username':'Nombre Usuario','first_name':'Nombre','last_name':'Apellido','active':_('Estado'),'userPais':'Nacionalidad', 'userTdni': "T.DNI",
                     'userProfesion': 'Profesión', 'numerodniUser': 'DNI', 'celUser' : 'TEL',
                     'last_login': 'Última sesión', 'created_by':'Creado por', 'created_on':'Creado el', 'changed_by':'Editado por', 'changed_on':'Editado el'}
    

    show_fieldsets = [
        (_('Información de usuario'),
         {'fields': ['username', 'active', 'roles', 'login_count', 'userPais']}),
        (_('Información personal'),
         {'fields': ['last_name', 'first_name', 'userProfesion', 'email','numerodniUser','celUser'], 'expanded': True}),
        (_('Registros'),
         {'fields': ['last_login', 'created_on',
                     'created_by', 'changed_on', 'changed_by'], 'expanded': False}),
    ]
    
    base_order = ('last_name','asc')  #  ordenar ('la columna', forma)

    search_columns = ['last_name', 'first_name', 'username', 'email', 'active', 'roles', 'celUser', 'userPais', 'userProfesion', 'numerodniUser']
   
    def get_state():
        return True
  
    base_filters = [['active', FilterEqualFunction, get_state]]
    

    list_title = 'Lista Usuarios'
    show_title = 'Detalle Usuario'
    add_title = 'Nuevo Usuario'
    edit_title = 'Editar Usuario'

    add_columns = [
        'last_name',
        'first_name',
        'username',
        'userProfesion',
        'active',
        'email',
        'celUser',
        'roles',
        'userPais', #muestro la User anidada
        'userTdni',
        'numerodniUser',
        'password',
        'conf_password'
    ]
    list_columns = [
        'last_name',
        'first_name',
        'username',
        'email',
        'active',
        'roles',
        'celUser',
        'userProfesion',
        'userTdni',
        'numerodniUser'
    ]
    edit_columns = [
        'last_name',
        'first_name',
        'username',
        'active',
        'email',
        'roles',
        'userProfesion',
        'celUser',
        'userPais', #muestro la User anidada
        'userTdni',
        'numerodniUser'
    ]

    validators_columns = {
        'numerodniUser':[Length(min = 8,max = 20,message = "Dato invalido.")]
    }
    

    base_order = ('last_name','asc')

    ##### para descargar la lista
    @action("down_excel","Descargar lista","","fa-file-excel-o",single=False)
    def down_excel(self, items):
        output = BytesIO()
        list_items = list()
        excel_columns = MyUserDBModelView.list_columns

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

        return send_file(output, attachment_filename='lista_usuarios' +fecha+ '.xlsx', as_attachment=True)
   
  