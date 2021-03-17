from flask import Flask, render_template, request, redirect, url_for, flash, session, make_response,Response,jsonify
from app import app,db,appbuilder
import pytz
from datetime import datetime
import random
import string
#MANEJADOR DE FECHAS
from dateutil.relativedelta import relativedelta

from app.plantas.models import Planta
from app.users.models import MyUser
from app.plan_usua.models import PlanUsua
from app.programarcarga.models import Programarcarga
from app.digestorsolido.models import Digestorsolido
from app.digestorliquido.models import Digestorliquido
from app.sustratos.models import Sustrato
from app.digestores.models import Digestor1
from app.plantaequipos.models import Plantaequipo
from app.superequipos.models import Superequipo
from app.tipoequipos.models import Tipoequipo


tz = pytz.timezone('America/Argentina/Buenos_Aires')


@app.route('/programarcargaview/add')
def ProgramarCarga():
    idplanta_session=str(session['idPlanta'])
    usuarios=db.session.query(MyUser.id,MyUser.first_name,MyUser.last_name,MyUser.numerodniUser).join(PlanUsua,PlanUsua.idUsuario==MyUser.id).filter(PlanUsua.idPlanta==idplanta_session).filter(PlanUsua.activoPlan_usua==1).all()
    digestores=db.session.query(Plantaequipo.idPlantaequipo,Plantaequipo.idSuperequipo,Plantaequipo.nombrePlantaequipo).join(Superequipo).join(Tipoequipo).filter(Superequipo.idTipoequipo=='1').filter(Plantaequipo.idPlanta==idplanta_session).all()
    sustratos=db.session.query(Sustrato).all()
    return render_template("programarcarga.html",usuarios=usuarios,digestores=digestores,sustratos=sustratos,base_template=appbuilder.base_template, appbuilder=appbuilder)

@app.route('/buscarSustratos',methods=['POST'])
def buscarSustratos():
    if request.method=='POST':
        data = request.get_json()
        data = data[0]
        idPlantaequipo=data['idPlantaequipo']
        SustratosSolidos=db.session.query(Digestorsolido,Sustrato).join(Sustrato,Digestorsolido.idsustrato==Sustrato.idSustrato).filter(Digestorsolido.idPlantaequipo==idPlantaequipo).group_by(Sustrato).all()
        SustratosLiquidos=db.session.query(Digestorliquido,Sustrato).join(Sustrato,Digestorliquido.idsustrato==Sustrato.idSustrato).filter(Digestorliquido.idPlantaequipo==idPlantaequipo).group_by(Sustrato).all()
        
        ListaSustSolidos=[]
        ListaSustLiquidos=[]
        for sus in SustratosSolidos:
            ListaSustSolidos.append((sus.Sustrato.idSustrato,sus.Sustrato.nombreSustrato))       
        for sus in SustratosLiquidos:
            ListaSustLiquidos.append((sus.Sustrato.idSustrato,sus.Sustrato.nombreSustrato))

        if len(ListaSustLiquidos)==0:
            return jsonify({'Mensaje':'Correcto','SustratosSolidos':ListaSustSolidos})
        else:
            return jsonify({'Mensaje':'Correcto','SustratosSolidos':ListaSustLiquidos})

@app.route('/guardarprogramacarga',methods=['POST'])
def guardarProgramaCarga():
    if request.method=='POST':
        #DATOS INDEPENDIENTES
        fechaInicio=request.form['fechaInicio']
        fechaInicio=datetime.strptime(fechaInicio, "%Y-%m-%d").date()

        fechaFinal= request.form['fechaFinal']
        fechaFinal=datetime.strptime(fechaFinal, "%Y-%m-%d").date()

        Tecnico=request.form['Tecnico']
        usuario_session=str(session['user_id'])
        FechaCarga=datetime.now(tz)
        #LISTADO DE INDICES RECIBIDOS
        listadeindices=request.form['cantidad'].split(',')
        
        #GENERO UN LISTADO DE FECHAS
        listadefechas=[]
        dias_totales = (fechaFinal-fechaInicio).days
        for days in range(dias_totales + 1): 
            fecha = fechaInicio + relativedelta(days=days)
            listadefechas.append(fecha)

        for li in listadeindices:
            Digestor=request.form['Digestor'+li]
            Sustrato=request.form['SustratoDigestor'+li]
            Valor=request.form['Valor'+li]
            for fecha in listadefechas:
                Carga=db.session.query(Programarcarga).filter(Programarcarga.idSustrato==Sustrato).filter(Programarcarga.idPlantaequipo==Digestor).filter(Programarcarga.fechaProgramarcarga==fecha).first()
                if Carga:
                    Carga.valorProgramacarga=Valor
                    db.session.commit()
                    mensajeUpdate=True
                else:
                    new_programacarga=(Programarcarga(fecha,Tecnico,Sustrato,Digestor,Valor,FechaCarga,usuario_session))                
                    db.session.add(new_programacarga)
                    db.session.commit()
                    mensajeInsert=True
        
        try:
            if (mensajeInsert==True):
                flash("Programación de Carga Finalizada","success")
        except:
            pass
        try :
            if (mensajeUpdate==True):
                flash("Hay registros que ya existian, los mismos fueron actualizados","success")    
        except:
            pass
        return redirect(url_for('ProgramarCarga'))