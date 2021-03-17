from flask import Flask, render_template, request, redirect, url_for, flash, session, make_response,Response
from app import app,db,appbuilder
from app.stsvs.models import Stsv
from app.plantas.models import Planta
from app.digestores.models import Digestor1
from app.users.models import MyUser
from app.plantaequipos.models import Plantaequipo
from app.superequipos.models import Superequipo
from app.tipoequipos.models import Tipoequipo
#from flask_mysqldb import MySQL
from datetime import datetime, date
import pytz
tz = pytz.timezone('America/Argentina/Buenos_Aires')



@app.route('/stsvview/add')
def stsvcargamasiva():
    usuario_session=str(session['user_id'])
    idplanta_session=str(session['idPlanta'])
    usuarios=db.session.query(MyUser).all()
    plantas=db.session.query(Planta).all()
    digestores=db.session.query(Digestor1).all()
    plantasjoin=db.session.query(Plantaequipo.idPlantaequipo,Plantaequipo.idSuperequipo,Plantaequipo.nombrePlantaequipo).join(Superequipo).join(Tipoequipo).filter(Superequipo.idTipoequipo=='1').filter(Plantaequipo.idPlanta==idplanta_session).all()
    return render_template("stsv.html",plantas=plantas,plantasjoin=plantasjoin,usuarios=usuarios,digestores=digestores,base_template=appbuilder.base_template, appbuilder=appbuilder)
    

@app.route('/confirmaCargaMasivaStsv', methods=["POST"])
def confirmaCargaMasivaStsv():
    control = 0 
    idplanta_session=str(session['idPlanta'])
    usuario_session=str(session['user_id'])
    plantasjoin=db.session.query(Plantaequipo.idPlantaequipo,Plantaequipo.idSuperequipo,Plantaequipo.nombrePlantaequipo).join(Superequipo).join(Tipoequipo).filter(Superequipo.idTipoequipo=='1').filter(Plantaequipo.idPlanta==idplanta_session).all()
    plantas=db.session.query(Planta).all()
    usuarios=db.session.query(MyUser).all()
    digestores=db.session.query(Digestor1).all()
    
    if request.method == 'POST':
        #USUARIO       
        usuario_session=str(session['user_id'])
        fechaMedicion = request.form['fechastsv']
        idUsuario = str(usuario_session)
        idUsuarioM = request.form['idUsuarioM']
        MsgCorrecto = ''
        MsgError = ''
        fechaCarga=datetime.now(tz)
       
        for plant in plantasjoin:
            idPlantaEquipo = plant.idPlantaequipo
            st = request.form['ST'+str(plant.idPlantaequipo)]
            sv = request.form['SV'+str(plant.idPlantaequipo)]
            Observaciones = request.form['Observaciones'+str(plant.idPlantaequipo)]         
           
            if st=='' or sv=='':
                MsgError = str(MsgError)+str(plant.nombrePlantaequipo)+","           
            else:     
                medicionafecha=db.session.query(Stsv).filter(Stsv.fechaStsv==fechaMedicion).filter(Stsv.idPlantaequipo==idPlantaEquipo).all()
                
                if medicionafecha:
                    flash("El digestor "+str(plant.nombrePlantaequipo)+" ya poseen datos cargados","danger")
                else:
                    control = control + 1
                    new_svst=(Stsv(fechaMedicion,idUsuario,st,sv,Observaciones,idUsuarioM,idPlantaEquipo,fechaCarga))
                    db.session.add(new_svst)
                    db.session.commit()
                    MsgCorrecto = str(MsgCorrecto)+ str(plant.nombrePlantaequipo)+","     
        
        if control != 0 :
            flash("Datos cargados correctamente para el/los Digestor/es :" + str(MsgCorrecto), "success")
            control = 0        
        if MsgError :
            flash("El/Los Digestor/es : "+str(MsgError)+" no poseen los datos suficientes para ser cargados","danger")
        return render_template('stsv.html',plantas=plantas, plantasjoin=plantasjoin, usuarios=usuarios, base_template=appbuilder.base_template, appbuilder=appbuilder)
