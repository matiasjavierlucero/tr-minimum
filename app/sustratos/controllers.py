from flask import Flask, render_template, request, redirect, url_for, flash, session, make_response,Response
from app import app,db,appbuilder
import pytz
from datetime import datetime
import random
import string
import os
from os import environ

@app.route('/chartMerma')
def popupMerma():
    planta_session=str(session['idPlanta'])
    entorno=str(session['ENTORNO'])
    puerto=environ.get('PORT')
    letters = string.ascii_lowercase
    winName = ''.join(random.choice(letters) for i in range(10))
    ruta = f'<script>var winDig = window.open("http://161.35.103.252:8050/charts/g_merma/{planta_session}", "{winName}", "height=640,left=400, titlebar=yes, toolbar=no, top=300, width=960,menubar=no,scrollbars=no,location=no,status=no"); winDig.document.title="Gráficos de Digestores"</script>'
    redi = f'<script>window.location.href = "http://{entorno}:{puerto}/programarcargaview/list";</script>'
    rutaMASredi = ruta + redi
    return rutaMASredi
