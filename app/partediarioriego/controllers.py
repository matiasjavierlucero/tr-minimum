from flask import Flask, render_template, request, redirect, url_for, flash, session, make_response,Response,jsonify
from app import app,db,appbuilder
from datetime import datetime,date
import random
import string
from dateutil.relativedelta import relativedelta

from app.users.models import MyUser
from app.plan_usua.models import PlanUsua
from app.lotes.models import Lote
from app.partediarioriego.models import Partediarioriego
from app.plantaequipos.models import Plantaequipo
from app.superequipos.models import Superequipo
from app.tipoequipos.models import Tipoequipo
from app.numturno.models import Numturno
from app.partediariolote.models import Partediariolote
from app.partediariotractor.models import Partediariotractor



import pytz
tz = pytz.timezone('America/Argentina/Buenos_Aires')


@app.route('/partediarioriegoview/add')
def Partediario_riego_add():
    usuario_session=str(session['user_id'])
    idplanta_session=str(session['idPlanta'])
    usuarios=db.session.query(MyUser.id,MyUser.first_name,MyUser.last_name,MyUser.numerodniUser).join(PlanUsua,PlanUsua.idUsuario==MyUser.id).filter(PlanUsua.idPlanta==idplanta_session).filter(PlanUsua.activoPlan_usua==1).all()
    lotes=db.session.query(Lote).filter(Lote.idPlanta==idplanta_session).all()
    tractores=db.session.query(Plantaequipo.idPlantaequipo,Plantaequipo.idSuperequipo,Plantaequipo.nombrePlantaequipo).join(Superequipo,Superequipo.idSuperequipo==Plantaequipo.idSuperequipo).join(Tipoequipo,Tipoequipo.idTipoequipo==Superequipo.idTipoequipo).filter(Superequipo.idTipoequipo==4).filter(Plantaequipo.idPlanta==idplanta_session).all()
    turnos=db.session.query(Numturno).all()
    print("LISTA DE TRACTORES ================>",tractores)
    return render_template('partediarioriego.html',usuarios=usuarios,lotes=lotes,tractores=tractores,turnos=turnos,base_template=appbuilder.base_template, appbuilder=appbuilder)

@app.route('/guardarParteDiarioRiego',methods=['POST'])
def Partediario_riego_guardar():
    if request.method=='POST':
        usuario_session=str(session['user_id'])
        idplanta_session=str(session['idPlanta'])
        usuarios=db.session.query(MyUser.id,MyUser.first_name,MyUser.last_name,MyUser.numerodniUser).join(PlanUsua,PlanUsua.idUsuario==MyUser.id).filter(PlanUsua.idPlanta==idplanta_session).filter(PlanUsua.activoPlan_usua==1).all()
        lotes=db.session.query(Lote).filter(Lote.idPlanta==idplanta_session).all()
        tractores=db.session.query(Plantaequipo.idPlantaequipo,Plantaequipo.idSuperequipo,Plantaequipo.nombrePlantaequipo).join(Superequipo,Superequipo.idSuperequipo==Plantaequipo.idSuperequipo).join(Tipoequipo,Tipoequipo.idTipoequipo==Superequipo.idTipoequipo).filter(Superequipo.idTipoequipo==4).filter(Plantaequipo.idPlanta==idplanta_session).all()
        turnos=db.session.query(Numturno).all()
        fecha=request.form['fecha']
        print(fecha)
        turno=request.form['idNumturno']
        print(turno)
        usuario=request.form['idUsuarioOP']
        print(usuario)
        observaciones=request.form['Observaciones']
        print(observaciones)
        fechacarga=datetime.now(tz)
        
        #VERIFICO QUE NO EXISTA PARTE EN LA FECHA SELECCIONADA
        partediario_turno=db.session.query(Partediarioriego).filter(Partediarioriego.idPlanta==idplanta_session).filter(Partediarioriego.fechaPartediarioriego==fecha).filter(Partediarioriego.idNumturno==turno).all()
        
        if partediario_turno:
            flash("Ya existe un parte para dicha fecha y turno","danger")
            return redirect(url_for('Partediario_riego_add'))


        #CREO LA SUPERCLASE Partediarioriego
        new_parteriego=(Partediarioriego(idplanta_session,fecha,observaciones,usuario,usuario_session,fechacarga,turno))
        db.session.add(new_parteriego)
        db.session.commit()
        #OBTENGO EL ID 
        ultimoparteriego_id=db.session.query(Partediarioriego).filter(Partediarioriego.idPlanta==idplanta_session).order_by(Partediarioriego.idPartediarioriego.desc()).first()
        print (ultimoparteriego_id.idPartediarioriego)
        ultimoid=ultimoparteriego_id.idPartediarioriego

        for lote in lotes:
            solidoLote=request.form[f'solido_{lote.idLote}']
            liquidoLote=request.form[f'liquido_{lote.idLote}']
            new_partelote=(Partediariolote(lote.idLote,solidoLote,liquidoLote,ultimoid))
            db.session.add(new_partelote)
            db.session.commit()

        for tractor in tractores:
            horasTractor=request.form[f'horas_{tractor.idPlantaequipo}']
            litrosTractor=request.form[f'litros_{tractor.idPlantaequipo}']
            print(horasTractor,litrosTractor)
        return render_template('partediarioriego.html',usuarios=usuarios,lotes=lotes,tractores=tractores,turnos=turnos,base_template=appbuilder.base_template, appbuilder=appbuilder)




@app.route('/partediarioriegoview/show')
def listado_parte_riego():
    print("ENTRO")
    return render_template('listadoriegolote.html', base_template=appbuilder.base_template, appbuilder=appbuilder)      