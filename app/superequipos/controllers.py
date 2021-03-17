from flask import Flask, g, render_template, request, redirect, url_for, flash, session, make_response,Response,jsonify
from app import app,db,appbuilder
from os import environ 
from app.plantas.models import Planta
from app.plan_usua.models import PlanUsua
from app.users.models import MyUser
from app.roles.models import MyRole, MyRoleUser
from app.marcas.models import Marca


@app.route('/guardarMarca', methods=['POST'])
def agregarmarca():
    if request.method=='POST':
        data = request.get_json()
        data = data[0]
        nombreMarca=data['marca']
        new_Marca=(Marca(nombreMarca))
        db.session.add(new_Marca)
        db.session.commit()
        flash('Nueva Marca Creada','success')
        print('Se guardo la marca')

    return jsonify({'Mensaje':'Correcto'})
