from flask import Flask, render_template, request, redirect, url_for, flash, session, make_response,Response,jsonify
from app import app,db,appbuilder
import pytz
from datetime import datetime
import random
import string

from app.users.models import MyUser
from app.plan_usua.models import PlanUsua
from app.plantas.models import Planta

tz = pytz.timezone('America/Argentina/Buenos_Aires')


@app.route('/inactiveusers')
def usuarioInactivos():
    usuario_session=str(session['user_id'])
    idplanta_session=str(session['idPlanta'])
    usuarios=db.session.query(MyUser.id,MyUser.first_name,MyUser.last_name,MyUser.numerodniUser).join(PlanUsua,PlanUsua.idUsuario==MyUser.id).filter(PlanUsua.idPlanta==idplanta_session).filter(PlanUsua.activoPlan_usua==0).all()
    for usuario in usuarios:
        print(usuario)
    return render_template("usuariosinactivos.html",usuarios=usuarios,base_template=appbuilder.base_template, appbuilder=appbuilder)

@app.route('/activarusuario/<id>')
def activarusuario(id):
    usuario=db.session.query(PlanUsua).filter(PlanUsua.idUsuario==id).first()
    usuario.activoPlan_usua=1
    db.session.commit()
    flash ("Usuario activado correctamente","success")
    return redirect(url_for('usuarioInactivos')) 


