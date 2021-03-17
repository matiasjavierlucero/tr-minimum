from flask_appbuilder.security.sqla.manager import SecurityManager
from .models import MyUser
from .views import MyUserDBModelView
from app.roles.models import MyRole
from app.roles.views import MyRoleDBModelView
# este bloque no se exactamente que funcion cumple . OJO
class MySecurityManager(SecurityManager):
    user_model = MyUser
    role_model = MyRole
    userdbmodelview = MyUserDBModelView
    rolemodelview = MyRoleDBModelView