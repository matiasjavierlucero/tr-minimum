from flask import Flask, render_template, request, redirect, url_for, flash, session, make_response,Response,jsonify
from app import app,db,appbuilder
from datetime import datetime,date
import random
import string

from app.users.models import MyUser
from app.campanias.models import Campania
from app.incrementocampania.models import Incremcampania
from app.plan_usua.models import PlanUsua
from app.sustratos.models import Sustrato
from app.digestorsolido.models import Digestorsolido
from app.scadas.models import Scada

import pytz
tz = pytz.timezone('America/Argentina/Buenos_Aires')


@app.route('/campaniaview/add')
def nuevacampania():
    usuario_session=str(session['user_id'])
    idplanta_session=str(session['idPlanta'])
    usuarios=db.session.query(MyUser.id,MyUser.first_name,MyUser.last_name,MyUser.numerodniUser).join(PlanUsua,PlanUsua.idUsuario==MyUser.id).filter(PlanUsua.idPlanta==idplanta_session).filter(PlanUsua.activoPlan_usua==1).all()
    sustratos=db.session.query(Sustrato).all()
    return render_template("nuevacampania.html",usuarios=usuarios,sustratos=sustratos,base_template=appbuilder.base_template, appbuilder=appbuilder)

@app.route('/guardarnuevacampania', methods=['POST'])
def guardarnuevacampania():
    if request.method == 'POST':
        
        usuario_session=str(session['user_id'])
        idplanta_session=str(session['idPlanta'])
        usuarios=db.session.query(MyUser.id,MyUser.first_name,MyUser.last_name,MyUser.numerodniUser).join(PlanUsua,PlanUsua.idUsuario==MyUser.id).filter(PlanUsua.idPlanta==idplanta_session).filter(PlanUsua.activoPlan_usua==1).all()
        sustratos=db.session.query(Sustrato).all()
        listadeindices=request.form['cantidad'].split(',')
        ##DATOS FIJOS
        FechaCreacion=request.form['fechaCreacion']
        UsuarioResponsable=request.form['idUsuarioR']
        NombreCampania=request.form['nombreCampania']
        FechaCarga=datetime.now(tz)
        #OBTENGO EL ID DE LA ULTIMA CAMPAÑA EXISTENTE; PARA LUEGO CERRARLA
        CampaniaTerminada=db.session.query(Campania).filter(Campania.idPlanta==idplanta_session).order_by(Campania.fechaCampania.desc()).first()
        
        #CREO LA CAMPAÑA
        new_campania=(Campania(NombreCampania,usuario_session,UsuarioResponsable,FechaCreacion,FechaCarga,idplanta_session,1))
        db.session.add(new_campania)
        db.session.commit()

        #CIERRO LA CAMPAÑA ANTERIOR
        if CampaniaTerminada :
            CampaniaTerminada.activoCampania=0
            db.session.commit()

        #OBTENGO EL ID DE LA NUEVA CAMPAÑA QUE AHORA ES LA ULTIMA CREADA
        idUltimacampania=db.session.query(Campania).filter(Campania.idPlanta==idplanta_session).order_by(Campania.idCampania.desc()).first()
        idUltimacampania=idUltimacampania.idCampania   
         
        for indice in listadeindices:
            idSustrato=request.form['idSustrato'+indice]
            restante=request.form['restante'+indice]
            cosechado=request.form['cosechado'+indice]
            valor=request.form['valor'+indice]
            cargateorica=request.form['cargateorica'+indice]
            
            new_incremCampania=(Incremcampania(idUltimacampania,UsuarioResponsable,FechaCreacion,0,restante,idSustrato,cosechado,valor,cargateorica,usuario_session,FechaCarga))
            db.session.add(new_incremCampania)
            db.session.commit() 

        flash ('Campaña Creada Correctamente','success')
        return redirect(url_for('CampaniaView.list'))


@app.route('/comprascampania')
def cargarincrementocampaniaid():
    #CAMPANIA ACTIVA
    usuario_session=str(session['user_id'])
    idplanta_session=str(session['idPlanta'])
    campanias=db.session.query(Campania).filter(Campania.idPlanta==idplanta_session).filter(Campania.activoCampania==1).first()
    if not campanias:
        campanias = []
        flash('De momento no existen campañas activas','warning')
        return render_template("cargarincremento.html", campanias=campanias, base_template=appbuilder.base_template, appbuilder=appbuilder)

    usuarios=db.session.query(MyUser.id,MyUser.first_name,MyUser.last_name,MyUser.numerodniUser).join(PlanUsua,PlanUsua.idUsuario==MyUser.id).filter(PlanUsua.idPlanta==idplanta_session).filter(PlanUsua.activoPlan_usua==1).all()
    idCampania=campanias.idCampania
    campanias=db.session.query(Campania).filter(Campania.idCampania==idCampania).first()
    
    sustratoscampania=db.session.query(Incremcampania,Sustrato,Campania).join(Campania,Campania.idCampania==Incremcampania.idCampania).join(Sustrato,Sustrato.idSustrato==Incremcampania.idSustrato).group_by(Incremcampania.idSustrato).filter(Incremcampania.idCampania==idCampania).all()
    fechainiciocampania=campanias.fechaCampania
    hoy=date.today()
    dias=hoy-fechainiciocampania
    dias=int(dias.days)
    #PARA EL MODAL TODOS LOS SUSTRATOS

    allSustratos=db.session.query(Sustrato).all()
    return render_template("cargarincremento.html",usuarios=usuarios,campanias=campanias,idCampania=idCampania,sustratoscampania=sustratoscampania,dias=dias,allSustratos=allSustratos,base_template=appbuilder.base_template, appbuilder=appbuilder)


@app.route("/guardarnuevosustratocampania",methods=["POST"])
def guardarnuevosustratocampania():
    if request.method=='POST':
        idSustratoNuevo=request.form['sustratonuevo']
        idUsuarioResponsable=request.form['usuarioSustratoNuevo']
        usuario_session=str(session['user_id'])
        idplanta_session=str(session['idPlanta'])
        idUltimacampania=db.session.query(Campania).filter(Campania.idPlanta==idplanta_session).order_by(Campania.idCampania.desc()).first()
        idUltimacampania=idUltimacampania.idCampania
        FechaCreacion=datetime.now(tz)   

        new_incremCampania=(Incremcampania(idUltimacampania,idUsuarioResponsable,FechaCreacion,0,0,idSustratoNuevo,0,0,0,usuario_session,FechaCreacion))
        db.session.add(new_incremCampania)
        db.session.commit() 
        flash('Se cargo un nuevo Sustrato a la Campaña, ahora ingrese los datos correspondientes','success')
        return redirect(url_for('cargarincrementocampaniaid'))


@app.route('/guardarincremento',methods=['POST'])
def guardarincremento():
    if request.method == 'POST':
        idplanta_session=str(session['idPlanta'])
        campanias=db.session.query(Campania).filter(Campania.idPlanta==idplanta_session).filter(Campania.activoCampania==1).first()
        idCampania=campanias.idCampania
        sustratoscampania=db.session.query(Incremcampania,Sustrato,Campania).join(Campania,Campania.idCampania==Incremcampania.idCampania).join(Sustrato,Sustrato.idSustrato==Incremcampania.idSustrato).filter(Incremcampania.idCampania==idCampania).group_by(Incremcampania.idSustrato).all()
        
        fechaIncremento=request.form['fechaIncremento']
        idUsuarioM=request.form['idUsuarioM']
        FechaCarga=datetime.now(tz)
        usuario_session=str(session['user_id'])
        print(request.form)
        for sustrato in sustratoscampania:
            idSustrato=sustrato.Incremcampania.idSustrato
            print(idSustrato)
            deposito=request.form['deposito'+str(idSustrato)]
            incremento=request.form['incremento'+str(idSustrato)]
            valor=request.form['valor'+str(idSustrato)]
            cargateorica=request.form['cargateorica'+str(idSustrato)]
            
            new_incremCampania=(Incremcampania(idCampania,idUsuarioM,fechaIncremento,1,deposito,idSustrato,incremento,valor,cargateorica,usuario_session,FechaCarga))
            #w_incremCampania=(Incremcampania(idUltimacampania,UsuarioResponsable,FechaCreacion,1,restante,idSustrato,cosechado,valor,cargateorica,usuario_session,FechaCarga))
            db.session.add(new_incremCampania)
            db.session.commit() 

        flash("Incremento Cargado Correctamente","success")
        return redirect(url_for('CampaniaView.list'))


@app.route('/restantes', methods=['POST'])
def rentastes():
    if request.method=='POST':
        idplanta_session=str(session['idPlanta'])
        data = request.get_json()
        data = data[0]
        campanias=db.session.query(Campania).filter(Campania.idPlanta==idplanta_session).filter(Campania.activoCampania==1).first()
        idCampania=campanias.idCampania
        fecha=data['fecha']
        fecha=datetime.strptime(fecha, "%Y-%m-%d").date()

        #0 Necesito saber los datos de conexion de la planta
        ScadaConnection=db.session.query(Scada).filter(Scada.idPlanta==idplanta_session).first()
        hostScada=ScadaConnection.hostScada
        usernameScada=ScadaConnection.usernameScada
        passScada=ScadaConnection.passScada
        nombredbScada=ScadaConnection.nombrebdScada

                
        import mysql.connector
        conn = mysql.connector.connect(user =usernameScada, password= passScada, host = hostScada,port='3306', database=nombredbScada)
        valores={}

        #1 Que sustratos involucra la campaña
        Sustratosdelacampania=[]
        sustratoscampania=db.session.query(Incremcampania.idSustrato).join(Campania,Campania.idCampania==Incremcampania.idCampania).join(Sustrato,Sustrato.idSustrato==Incremcampania.idSustrato).filter(Incremcampania.idCampania==idCampania).group_by(Incremcampania.idSustrato).all()
        for sustratodecampania in sustratoscampania:
            Sustratosdelacampania.append(sustratodecampania.idSustrato) 
        
        #2 Obtengo todos los nombres de las tablas de la Planta de Scada que utilizan el sustrato 
        for SusCam in Sustratosdelacampania:
            ultimoregistrosustrato=db.session.query(Incremcampania).filter(Incremcampania.idSustrato==SusCam).filter(Incremcampania.idCampania==idCampania).order_by(Incremcampania.fechaIncremcampania.desc()).first()
            fechainiciocampania=str(ultimoregistrosustrato.fechaIncremcampania) + ' 00:00:00'
            fecha=str(fecha)+' 23:59:59'
            if fecha < fechainiciocampania:
                return jsonify({"Mensaje":"Incorrecto","FechaInicio":fechainiciocampania})
            tablasScada=db.session.query(Digestorsolido.tablaDigestorsolido,Digestorsolido.campoDigestorsolido).filter(Digestorsolido.idPlanta==idplanta_session).filter(Digestorsolido.idsustrato==SusCam).all()
            #3 Ahora que tengo los nombres de las tablas, voy al Scada y obtengo todos los valores de cada tabla, y los sumo
            suma=0
            for tabScada in tablasScada:
                print('1')
                cur = conn.cursor()
                query=f'SELECT SUM({tabScada[1]}) FROM {tabScada[0]} WHERE Time_Stamp BETWEEN "{fechainiciocampania}" AND "{fecha}"'
                print('2')
                try:
                    cur.execute (query)
                except:
                    flash(f'La Tabla {tabScada[0]}, no fue encontrada en la base de datos {nombredbScada}','danger')
                    return jsonify({"Mensaje":"Error"})
                print('3')
                result = cur.fetchall()
                print('4')
                if len(result)>0:
                    print('5')
                    result=result[0][0]
                    if result==None:
                        result=0
                    suma=suma+result
                
            if suma<0:
                suma=0
            valores['deposito'+str(ultimoregistrosustrato.idSustrato)]=suma
        
        print (valores)
        print("############FIN DE LA EJECUCION ############")
        return jsonify({"Mensaje":"Correcto","Valores":valores})


#INFO DE LA CAMPAÑA
@app.route('/campaniaview/show/<id>')
def infocampania(id):
    campania=db.session.query(Campania,MyUser).join(MyUser,MyUser.id==Campania.idUsuarioM).filter(Campania.idCampania==id).first()
    incrementos=db.session.query(Incremcampania,Sustrato).join(Campania,Campania.idCampania==Incremcampania.idCampania).join(Sustrato,Sustrato.idSustrato==Incremcampania.idSustrato).filter(Incremcampania.idCampania==id).all()

    return render_template('infocampania.html',campania=campania,incrementos=incrementos,base_template=appbuilder.base_template, appbuilder=appbuilder)
