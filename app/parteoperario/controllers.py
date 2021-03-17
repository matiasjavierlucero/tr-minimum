from flask import Flask, render_template, request, redirect, url_for, flash, session, make_response,Response,jsonify
from app import app,db,appbuilder
import pytz
from datetime import datetime
import random
import string

from app.plantas.models import Planta
from app.users.models import MyUser
from app.plan_usua.models import PlanUsua
from app.superequipos.models import Superequipo
from app.tipoequipos.models import Tipoequipo
from app.plantaequipos.models import Plantaequipo
from app.parteoperario.models import Parteoperario
from app.numturno.models import Numturno
from app.partediariodigestor.models import Partediariodigestor
from app.partediariomotor.models import Partediariomotor
from app.partediariojcb.models import Partediariojcb

tz = pytz.timezone('America/Argentina/Buenos_Aires')


@app.route('/parteoperarioview/add')
def cargarParteOperario():
    usuario_session=str(session['user_id'])
    idplanta_session=str(session['idPlanta'])
    usuarios=db.session.query(MyUser.id,MyUser.first_name,MyUser.last_name).join(PlanUsua, PlanUsua.id == MyUser.id ).filter(PlanUsua.idPlanta==idplanta_session).all()
    plantas=db.session.query(Planta).filter(Planta.idPlanta==idplanta_session).all()
    turnos=db.session.query(Numturno).all()
    plantasjoin=db.session.query(Plantaequipo.idPlantaequipo,Plantaequipo.idSuperequipo,Plantaequipo.nombrePlantaequipo).join(Superequipo,Superequipo.idSuperequipo==Plantaequipo.idSuperequipo).join(Tipoequipo,Tipoequipo.idTipoequipo==Superequipo.idTipoequipo).filter(Superequipo.idTipoequipo=='1').filter(Plantaequipo.idPlanta==idplanta_session).all()
    motoresjoin=db.session.query(Plantaequipo.idPlantaequipo,Plantaequipo.idSuperequipo,Plantaequipo.nombrePlantaequipo).join(Superequipo,Superequipo.idSuperequipo==Plantaequipo.idSuperequipo).join(Tipoequipo,Tipoequipo.idTipoequipo==Superequipo.idTipoequipo).filter(Superequipo.idTipoequipo=='2').filter(Plantaequipo.idPlanta==idplanta_session).all()
    palascargadorasjoin=db.session.query(Plantaequipo.idPlantaequipo,Plantaequipo.idSuperequipo,Plantaequipo.nombrePlantaequipo).join(Superequipo,Superequipo.idSuperequipo==Plantaequipo.idSuperequipo).join(Tipoequipo,Tipoequipo.idTipoequipo==Superequipo.idTipoequipo).filter(Superequipo.idTipoequipo=='24').filter(Plantaequipo.idPlanta==idplanta_session).all()
    return render_template("cargarparteoperario.html",plantas=plantas,turnos=turnos,plantasjoin=plantasjoin,motores=motoresjoin,palascargadoras=palascargadorasjoin,usuarios=usuarios,base_template=appbuilder.base_template, appbuilder=appbuilder)

@app.route('/guardarParteOperario', methods=["POST"])
def guardarParteOperario():
    if request.method == 'POST':
        usuario_session=str(session['user_id'])
        idplanta_session=str(session['idPlanta'])
        usuarios=db.session.query(MyUser.id,MyUser.first_name,MyUser.last_name).join(PlanUsua,PlanUsua.idUsuario==MyUser.id).filter(PlanUsua.idPlanta==idplanta_session).all()            
        plantas=db.session.query(Planta).filter(Planta.idPlanta==idplanta_session).all()
        turnos=db.session.query(Numturno).all()
        plantasjoin=db.session.query(Plantaequipo.idPlantaequipo,Plantaequipo.idSuperequipo,Plantaequipo.nombrePlantaequipo).join(Superequipo,Superequipo.idSuperequipo==Plantaequipo.idSuperequipo).join(Tipoequipo,Tipoequipo.idTipoequipo==Superequipo.idTipoequipo).filter(Superequipo.idTipoequipo=='1').filter(Plantaequipo.idPlanta==idplanta_session).all()
        motoresjoin=db.session.query(Plantaequipo.idPlantaequipo,Plantaequipo.idSuperequipo,Plantaequipo.nombrePlantaequipo).join(Superequipo,Superequipo.idSuperequipo==Plantaequipo.idSuperequipo).join(Tipoequipo,Tipoequipo.idTipoequipo==Superequipo.idTipoequipo).filter(Superequipo.idTipoequipo=='2').filter(Plantaequipo.idPlanta==idplanta_session).all()
        palascargadorasjoin=db.session.query(Plantaequipo.idPlantaequipo,Plantaequipo.idSuperequipo,Plantaequipo.nombrePlantaequipo).join(Superequipo,Superequipo.idSuperequipo==Plantaequipo.idSuperequipo).join(Tipoequipo,Tipoequipo.idTipoequipo==Superequipo.idTipoequipo).filter(Superequipo.idTipoequipo=='24').filter(Plantaequipo.idPlanta==idplanta_session).all()

        ##Datos Fijos
        fechaParteOperario = request.form['fechaParteOperario']
        idUsuarioOP = request.form['idUsuarioOP']
        turno=request.form['turno']
        idUsuario = str(session['user_id'])
        fechaCarga=datetime.now(tz)
        Observaciones = request.form['observaciones']
        
        #VERIFICO SI YA EXISTE UN PARTE PARA LA FECHA Y TURNO
        partediarioControl=db.session.query(Parteoperario).filter(Parteoperario.fechaParteoperario==fechaParteOperario).filter(Parteoperario.idNumturno==turno).all()
        for parte in partediarioControl:
            print(parte.idParteoperario)
        if partediarioControl:
            flash('Ya existe un parte para este Turno en el Dia','danger')
            return redirect(url_for('cargarParteOperario'))


        ##CREO EL PARTE
        new_parteOperario=(Parteoperario(idplanta_session, idUsuarioOP,fechaParteOperario,turno,Observaciones,idUsuario,fechaCarga))
        db.session.add(new_parteOperario)
        db.session.commit()
        
        ##OBTENGO EL ID DEL ULTIMO PARTE -->Necesario para el resto de los partes (MOTORES; DIGESTORES; PALAS)
        idUltimoParte=db.session.query(Parteoperario).order_by(Parteoperario.idParteoperario.desc()).first()
        idUltimoParte=idUltimoParte.idParteoperario

        ##Datos Variables
        
        ##COSTRA ESPUMA
        for plant in plantasjoin:
            idPlantaEquipo = str(plant.idPlantaequipo)
            try:
                Costra=request.form['costradigestor'+str(plant.idPlantaequipo)+'']
                if Costra=='on':
                    Costra=1
            except :
                Costra=0
           
            try:
                Espuma=request.form['espumadigestor'+str(plant.idPlantaequipo)+'']
                if Espuma=='on':
                    Espuma=1
            except :
                Espuma=0
            
            new_parteDigestor=(Partediariodigestor(idPlantaEquipo, Costra,Espuma,idUltimoParte))
            db.session.add(new_parteDigestor)
            db.session.commit()


        ##MOTORES
        for motores in motoresjoin:
            idPlantaEquipo=str(motores.idPlantaequipo)
            gasoilMotor=request.form['motor'+str(motores.idPlantaequipo)]
            print ("Gasoil de Motor", gasoilMotor)
            new_parteMotor=(Partediariomotor(idPlantaEquipo,gasoilMotor,idUltimoParte))
            db.session.add(new_parteMotor)
            db.session.commit()


        ##PALAS CARGDORAS GASOIL y HORAS
        for palas in palascargadorasjoin:
            idPlantaEquipo=str(palas.idPlantaequipo)
            gasoilPala=request.form['gasoilPala'+str(palas.idPlantaequipo)]
            horasPala=request.form['horasPala'+str(palas.idPlantaequipo)]
            print ("Horas de Pala", horasPala)
            print ("Gasoil de Pala", gasoilPala)
            new_parteJcb=(Partediariojcb(idPlantaEquipo,gasoilPala,horasPala,idUltimoParte))
            db.session.add(new_parteJcb)
            db.session.commit()
        
        flash('Parte Cargado Correctamente','success')
        return redirect(url_for('cargarParteOperario'))
 

@app.route('/parteoperarioview/edit/<id>')
def editarPartesPlanta(id):
    usuario_session=str(session['user_id'])
    idplanta_session=str(session['idPlanta'])
    usuarios=db.session.query(MyUser.id,MyUser.first_name,MyUser.last_name).join(PlanUsua,PlanUsua.idUsuario==MyUser.id).filter(PlanUsua.idPlanta==idplanta_session).all()
    plantas=db.session.query(Planta).filter(Planta.idPlanta==idplanta_session).all()
    turnos=db.session.query(Numturno).all()
    #plantasjoin=db.session.query(Plantaequipo.idPlantaequipo,Plantaequipo.idSuperequipo,Plantaequipo.nombrePlantaequipo).join(Superequipo).join(Tipoequipo).filter(Superequipo.idTipoequipo=='1').filter(Plantaequipo.idPlanta==idplanta_session).all()
    #motoresjoin=db.session.query(Plantaequipo.idPlantaequipo,Plantaequipo.idSuperequipo,Plantaequipo.nombrePlantaequipo).join(Superequipo).join(Tipoequipo).filter(Superequipo.idTipoequipo=='2').filter(Plantaequipo.idPlanta==idplanta_session).all()
    #palascargadorasjoin=db.session.query(Plantaequipo.idPlantaequipo,Plantaequipo.idSuperequipo,Plantaequipo.nombrePlantaequipo).join(Superequipo).join(Tipoequipo).filter(Superequipo.idTipoequipo=='24').filter(Plantaequipo.idPlanta==idplanta_session).all()
    
    idParte=id
    datosfijosparte=db.session.query(Parteoperario,MyUser,Numturno).join(MyUser,Parteoperario.idUsuarioOP==MyUser.id).join(Numturno).order_by(Parteoperario.fechaParteoperario.desc()).order_by(Parteoperario.idNumturno.asc()).filter(Parteoperario.idParteoperario==idParte).first()
    partedigestor=db.session.query(Parteoperario,Partediariodigestor,Plantaequipo).join(Partediariodigestor,Partediariodigestor.idParteopeario==Parteoperario.idParteoperario).join(Plantaequipo,Plantaequipo.idPlantaequipo==Partediariodigestor.idPlantaequipo).order_by(Parteoperario.fechaParteoperario.desc()).order_by(Parteoperario.idNumturno.asc()).filter(Parteoperario.idParteoperario==idParte).all()
    partemotor=db.session.query(Parteoperario,Partediariomotor,Plantaequipo).join(Partediariomotor,Partediariomotor.idParteoperario==Parteoperario.idParteoperario).join(Plantaequipo,Plantaequipo.idPlantaequipo==Partediariomotor.idPlantaequipo).order_by(Parteoperario.fechaParteoperario.desc()).order_by(Parteoperario.idNumturno.asc()).filter(Parteoperario.idParteoperario==idParte).all()
    partejcb=db.session.query(Parteoperario,Partediariojcb,Plantaequipo).join(Partediariojcb,Partediariojcb.idParteoperario==Parteoperario.idParteoperario).join(Plantaequipo,Plantaequipo.idPlantaequipo==Partediariojcb.idPlantaequipo).order_by(Parteoperario.fechaParteoperario.desc()).order_by(Parteoperario.idNumturno.asc()).filter(Parteoperario.idParteoperario==idParte).all()
  
    return render_template("editarparteoperario.html",datosfijosparte=datosfijosparte,partedigestor=partedigestor,partemotor=partemotor,partejcb=partejcb,plantas=plantas,turnos=turnos,usuarios=usuarios,base_template=appbuilder.base_template, appbuilder=appbuilder)


@app.route('/guardarCambiosParteOperario/<id>', methods=["POST"])
def guardarCambiosParteOperario(id):
    if request.method == 'POST':
        usuario_session=str(session['user_id'])
        idplanta_session=str(session['idPlanta'])
        usuarios=db.session.query(MyUser.id,MyUser.first_name,MyUser.last_name).join(PlanUsua,PlanUsua.idUsuario==MyUser.id).filter(PlanUsua.idPlanta==idplanta_session).all()
        plantas=db.session.query(Planta).filter(Planta.idPlanta==idplanta_session).all()
        turnos=db.session.query(Numturno).all()
        #plantasjoin=db.session.query(Plantaequipo.idPlantaequipo,Plantaequipo.idSuperequipo,Plantaequipo.nombrePlantaequipo).join(Superequipo).join(Tipoequipo).filter(Superequipo.idTipoequipo=='1').filter(Plantaequipo.idPlanta==idplanta_session).all()
        #motoresjoin=db.session.query(Plantaequipo.idPlantaequipo,Plantaequipo.idSuperequipo,Plantaequipo.nombrePlantaequipo).join(Superequipo).join(Tipoequipo).filter(Superequipo.idTipoequipo=='2').filter(Plantaequipo.idPlanta==idplanta_session).all()
        #palascargadorasjoin=db.session.query(Plantaequipo.idPlantaequipo,Plantaequipo.idSuperequipo,Plantaequipo.nombrePlantaequipo).join(Superequipo).join(Tipoequipo).filter(Superequipo.idTipoequipo=='24').filter(Plantaequipo.idPlanta==idplanta_session).all()
        
        idParte=id
        datosfijosparte=db.session.query(Parteoperario,MyUser,Numturno).join(MyUser,Parteoperario.idUsuarioOP==MyUser.id).join(Numturno).order_by(Parteoperario.fechaParteoperario.desc()).order_by(Parteoperario.idNumturno.asc()).filter(Parteoperario.idParteoperario==idParte).first()
        partedigestor=db.session.query(Parteoperario,Partediariodigestor,Plantaequipo).join(Partediariodigestor,Partediariodigestor.idParteopeario==Parteoperario.idParteoperario).join(Plantaequipo,Plantaequipo.idPlantaequipo==Partediariodigestor.idPlantaequipo).order_by(Parteoperario.fechaParteoperario.desc()).order_by(Parteoperario.idNumturno.asc()).filter(Parteoperario.idParteoperario==idParte).all()
        partemotor=db.session.query(Parteoperario,Partediariomotor,Plantaequipo).join(Partediariomotor,Partediariomotor.idParteoperario==Parteoperario.idParteoperario).join(Plantaequipo,Plantaequipo.idPlantaequipo==Partediariomotor.idPlantaequipo).order_by(Parteoperario.fechaParteoperario.desc()).order_by(Parteoperario.idNumturno.asc()).filter(Parteoperario.idParteoperario==idParte).all()
        partejcb=db.session.query(Parteoperario,Partediariojcb,Plantaequipo).join(Partediariojcb,Partediariojcb.idParteoperario==Parteoperario.idParteoperario).join(Plantaequipo,Plantaequipo.idPlantaequipo==Partediariojcb.idPlantaequipo).order_by(Parteoperario.fechaParteoperario.desc()).order_by(Parteoperario.idNumturno.asc()).filter(Parteoperario.idParteoperario==idParte).all()
        
        ##Datos Fijos
        fechaParteOperario = request.form['fechaParteOperario']
        idUsuarioOP = request.form['idUsuarioOP']
        turno=request.form['turno']
        idUsuario = str(session['user_id'])
        fechaCarga=datetime.now(tz)
        Observaciones = request.form['observaciones']
        

        
        #AL INTENTAR GUARDAR DEBO VERIFICAR QUE EL TURNO SEA EL MISMO; SI ES OTRO DEBO VERIFICAR QUE NO EXISTA YA
        partediarioControl=db.session.query(Parteoperario).filter(Parteoperario.idParteoperario==id).first()
        #Verifico si el turno es el mismo que se quiere editar
        if str(partediarioControl.idNumturno)==str(turno):
            pass
        else:
            #VERIFICO SI YA EXISTE UN PARTE PARA LA FECHA Y TURNO
            partediarioControlturno=db.session.query(Parteoperario).filter(Parteoperario.fechaParteoperario==fechaParteOperario).filter(Parteoperario.idNumturno==turno).first()
            if partediarioControlturno:
                flash('Ya existe un parte para este Turno en el Dia','danger')
                return redirect(url_for('editarPartesPlanta',id=id))
            else:
                pass

        
        #Actualizo la fecha
        partediarioControl.idNumturno=turno
        partediarioControl.fechaParteoperario=fechaParteOperario
        partediarioControl.idUsuarioOP=idUsuarioOP
        partediarioControl.obsParteoperario=Observaciones
        db.session.commit()

        #Actualizacion Parte digestor (COSTRA y ESPUMA)
        for digestor in partedigestor:
            idPlanta_equipo=digestor.Plantaequipo.idPlantaequipo
            idParte_digestor=digestor.Partediariodigestor.idPartediariodigestor
            try:
                Costra=request.form['costradigestor'+str(idPlanta_equipo)+'']
                if Costra=='on':
                    Costra=1
            except :
                Costra=0
           
            try:
                Espuma=request.form['espumadigestor'+str(idPlanta_equipo)+'']
                if Espuma=='on':
                    Espuma=1
            except :
                Espuma=0

            print(Costra)
            print(Espuma)
            partedigestorUpdate=db.session.query(Partediariodigestor).filter(Partediariodigestor.idPartediariodigestor==idParte_digestor).first()
            partedigestorUpdate.costraPartediariodigestor=Costra
            partedigestorUpdate.espumaPartediariodigestor=Espuma
            db.session.commit()

        #ACTUALIZACION PARTE MOTOR
        for motor in partemotor:
            idPlanta_equipo=motor.Plantaequipo.idPlantaequipo
            idParte_motor=motor.Partediariomotor.idPartediariomotor
            gasoilMotor=request.form['motor'+str(idPlanta_equipo)]
            print(idPlanta_equipo)
            print(idParte_motor)
            partemotorUpdate=db.session.query(Partediariomotor).filter(Partediariomotor.idPartediariomotor==idParte_motor).first()
            partemotorUpdate.gasoilPartediariomotor=gasoilMotor
            db.session.commit()

        for pala in partejcb:
            idPlanta_equipo=pala.Plantaequipo.idPlantaequipo
            idParte_jcb=pala.Partediariojcb.idPartediariojcb
            gasoilPala=request.form['gasoilPala'+str(idPlanta_equipo)]
            horasPala=request.form['horasPala'+str(idPlanta_equipo)]
            partepalaUpdate=db.session.query(Partediariojcb).filter(Partediariojcb.idPartediariojcb==idParte_jcb).first()
            partepalaUpdate.gasoilPartediariojcb=gasoilPala
            partepalaUpdate.horasPartediariojcb=horasPala
            db.session.commit()

        flash('Parte Actualizado Correctamente','success')
        return redirect(url_for('editarPartesPlanta',id=id))
