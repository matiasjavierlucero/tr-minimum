from flask import session
from flask_appbuilder import ModelView,expose,action
from flask_appbuilder.models.sqla.interface import SQLAInterface
from app import appbuilder
from flask_babelpkg import lazy_gettext as _
from flask_appbuilder.security.views import UserDBModelView
from wtforms.validators import Length, NumberRange, AnyOf, NoneOf, Regexp
# para aplicar filtro por defecto 

from flask_appbuilder.models.sqla.filters import FilterEqualFunction,FilterStartsWith
####################
from app.plan_usua.models import PlanUsua ####### import del MODEL de pais

###########

class PlanUsuaView(ModelView):
    datamodel = SQLAInterface(PlanUsua)

    label_columns = {'username':'Nombre Usuario','first_name':'Nombre','last_name':'Apellido','userPais':'Nacionalidad', 'userTdni': "Tipo Doc.",
                     'userProfesion': 'Profesión', 'numerodniUser': 'DNI', 'celUser' : 'Tel.',
                     'last_login': 'Última sesión', 'created_by':'Creado por', 'created_on':'Creado el', 'changed_by':'Editado por', 'changed_on':'Editado el',
                     'fcargaPlan_usua':'Fecha de Carga','finicioPlan_usua':'Fecha Inicio Usuario','activoPlan_usua':'Activo'}

    search_columns = ['last_name', 'first_name', 'username', 'email', 'active', 'roles', 'celUser', 'userPais', 'userProfesion', 'numerodniUser']  
    order_columns = ['last_name', 'first_name', 'username', 'email', 'active', 'roles', 'userProfesion', 'userTdni'] #columnas ordenables

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
   
    def get_state():
        return True
    
    def get_planta():
        return str(session['idPlanta'])
        
  
    base_filters = [['activoPlan_usua', FilterEqualFunction, get_state],['idPlanta',FilterEqualFunction, get_planta]]

    list_title = 'Lista Usuarios'
    show_title = 'Detalle Usuario'
    add_title = 'Nuevo Usuario'
    edit_title = 'Editar Usuario'

    add_columns = [
        'last_name',
        'first_name',
        'username',
        'userProfesion',
        'email',
        'celUser',
        'roles',
        'userPais', #muestro la User anidada
        'userTdni',
        'numerodniUser',
        'password',
        'finicioPlan_usua',
        'activoPlan_usua'
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
        'email',
        'roles',
        'userProfesion',
        'celUser',
        'userPais', #muestro la User anidada
        'userTdni',
        'numerodniUser',
        'finicioPlan_usua',
        'activoPlan_usua'
    ]

    add_exclude_columns=['fcargaPlan_usua', 'active']
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
   
  

usuario_planta_builder = appbuilder.add_view(
    PlanUsuaView,
    "Plantas del usuario"

)
