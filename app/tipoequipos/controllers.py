from flask import Flask, g, render_template, request, redirect, url_for, flash, session, make_response,Response,jsonify
from app import app,db,appbuilder
from os import environ 
from app.plantas.models import Planta
from app.plan_usua.models import PlanUsua
from app.users.models import MyUser
from app.roles.models import MyRole, MyRoleUser
from app.tipoequipos.models import Tipoequipo
from app.plantaequipos.models import Plantaequipo
# PARA OBTENER LA URL DEL ENTORNO, YA SEA LOCALHOST O PRODUCCIÓN. COnfigurar .env
ENTORNO = environ.get('ENTORNO')

def get_user_id():
    return g.user.id


@app.route('/tequipos/list/')
def listado_tequipos():
    tequipos = db.session.query(Tipoequipo).order_by(Tipoequipo.nombreTipoequipo.asc()).all()
    idPlanta = session["idPlanta"]
    planta_equipos = db.session.query(Plantaequipo).filter(Plantaequipo.idPlanta == idPlanta).all()
    return render_template("tequipos.html", tequipos = tequipos, base_template=appbuilder.base_template, appbuilder=appbuilder)

@app.route('/NuevoTipoEquipo', methods=['POST'])
def crearTipoequipo():
    if request.method=='POST':
        data = request.get_json()
        data = data[0]
        nombre=str(data['nombre'])
        print (nombre)
        new_TipoEquipo=(Tipoequipo(nombre))
        db.session.add(new_TipoEquipo)
        db.session.commit()
        flash('Nuevo Tipo de Equipo Creado','success')
        print('Se guardo la marca')

        return jsonify({'Mensaje':'Correcto'})


@app.route('/eliminartipoequipo/<id>/')
def eliminar_tequipos(id):
    id=str(id)
    tequipos = db.session.query(Tipoequipo).filter(Tipoequipo.idTipoequipo==id).first()
    print (tequipos)
    try:
        db.session.delete(tequipos)
        db.session.commit()
        flash('Tipo de Equipo Eliminado','danger')
    except:
        flash('El Tipo de Equipo esta asignado a un Equipo , NO PUEDE ELIMINARLO','danger')
    
    
    return redirect(url_for('listado_tequipos'))
