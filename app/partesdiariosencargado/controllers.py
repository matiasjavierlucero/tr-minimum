from flask import Flask, render_template, request, redirect, url_for, flash, session, make_response,Response,jsonify
from app import app,db,appbuilder
import pytz
from datetime import datetime
import random
import string

from app.plantas.models import Planta
from app.users.models import MyUser
from app.partesdiariosencargado.models import Parteencargado
from app.plan_usua.models import PlanUsua


tz = pytz.timezone('America/Argentina/Buenos_Aires')


@app.route('/parteencargadoview/add')
def ParteDiarioEncargado():
    usuario_session=str(session['user_id'])
    idplanta_session=str(session['idPlanta'])
    usuarios=db.session.query(MyUser).all()
    usuariosplanta=db.session.query(MyUser.id,MyUser.first_name,MyUser.last_name).join(PlanUsua, PlanUsua.id == MyUser.id).filter(PlanUsua.idPlanta==idplanta_session).all()

    return render_template("partediarioencargado.html",usuarios=usuarios,usuariosplanta=usuariosplanta,base_template=appbuilder.base_template, appbuilder=appbuilder)


@app.route('/guardarParteDiarioEncargado', methods=["POST"])
def guardarParteDiarioEncargado():
    if request.method == 'POST':
        usuario_session=str(session['user_id'])
        idplanta_session=str(session['idPlanta'])
        usuarios=db.session.query(MyUser).all()
        usuariosplanta=db.session.query(MyUser.id,MyUser.first_name,MyUser.last_name).join(PlanUsua,PlanUsua.idUsuario==MyUser.id).filter(PlanUsua.idPlanta==idplanta_session).all()

        fechaParteDiarioEncargado = request.form['fechaParteDiarioEncargado']
        idUsuarioOP = request.form['idUsuarioOP']
        ObsParteDiarioEncargado = request.form['ObsParteDiarioEncargado']
        idUsuario = str(session['user_id'])
        fechaCarga=datetime.now(tz)
        print(fechaParteDiarioEncargado,idUsuarioOP,ObsParteDiarioEncargado,idUsuario,fechaCarga)

        new_parteEncargado=(Parteencargado(idplanta_session, fechaCarga, ObsParteDiarioEncargado,idUsuarioOP,idUsuario,fechaParteDiarioEncargado))
        db.session.add(new_parteEncargado)
        db.session.commit()
        flash('Parte Cargado Correctamente','success')
        return redirect(url_for('ParteDiarioEncargado'))
