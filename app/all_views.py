from flask import render_template
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import ModelView, ModelRestApi, MultipleView, MasterDetailView, BaseView,expose, action, has_access

################## EN ESTE BLOQUE TENDRÍA Q IMPORTAR TODAS LAS VIEWS ##################
#from app.consultoras.views import ConsultoraView, consultoras_builder # importamos view y builder de operator
from app.users.views import MyUserDBModelView  # el model del usuario para agregar columnas a ab_user
from app.roles.views import MyRoleDBModelView
from app.consultoras.views import ConsultoraView,consultoras_builder
from app.paises.views import PaisView, paises_builder
from app.provincias.views import ProvinciaView, provincias_builder
from app.localidades.views import LocalidadView, localidades_builder
from app.tdnis.views import TdniView, tdnis_builder
from app.profesiones.views import ProfesionView, profesiones_builder
from app.plantas.views import PlantaView, Plantas_builder, MisPlantasView, MisPlantas_builder
from app.areas.views import AreaView,areas_builder
from app.plan_usua.views import PlanUsuaView, usuario_planta_builder
from app.area_plan.views import Area_PlanView,areas_planta_builder
from app.marcas.views import MarcaView, marcas_builder
from app.tipoequipos.views import TipoequipoView, tipoequipos_builder
from app.superequipos.views import SuperequipoView, superequipos_builder
from app.plantaequipos.views import PlantaequipoView, plantaequipos_builder, EquiposPlantaView
from app.estadoqs.views import EstadoqView, estadoqs_builder
#A
from app.agitadores.views import Agitador16View, agitador16_builder
from app.analisisquimicos.views import Analisisquimico,analisisquimico_builder
from app.analizadorgas.views import Analizadorgas17View, analizadorgas17_builder
from app.antorchas.views import Antorcha11View, antorcha11_builder
from app.analisistrazas.views import AnalisistrazaView, analisistraza_builder
#B
from app.bombas.views import Bomba5View, bomba5_builder
#C
from app.calderas.views import caldera6_builder,Caldera6View
from app.campanias.views import NuevaCampaniaView, campania_builder,CampaniaView,camp_builder
from app.caudalimetros.views import Caudalimetro26View, caudalimetros_builder
from app.cargamermas.views import CargamermaView,cargamerma_builder
from app.chillers.views import Chiller13View, chiller13_builder
from app.combustibles.views import CombustibleView,combustibles_builder
from app.compresoraire.views import Compresoraire22, compresoraire22_builder
from app.chartScada.views import incaView,chart_inca_builder
#D
from app.depositos.views import Deposito14View, deposito14_builder
from app.desulfurizadores.views import Desulfurizador18View,desulfurizador18_builder
from app.digestores.views import Digestor1View, digestor1_builder
from app.digestorliquido.views import DigestorliquidoView, digestorliquido_builder
from app.digestorsolido.views import DigestorsolidoView, digestorsolido_builder
#F
from app.fostac.views import FostacView, fostac_builder, ChartView, chart_builder, fostacmasiva_builder, CargaMasivaView
from app.filtrobiogases.views import Filtrobiogas19View,filtrobiogas19_builder
#I
from app.intdecalors.views import intdecalor7_builder, Intdecalor7View
from app.incascada.views import incaScada_builder,IncaScadaView
#L
from app.lotes.views import LoteView, Lote_builder
#M
from app.motores.views import Motor2View, motor2_builder,motoresView,chart_motor_builder
#P
from app.palas.views import Palacargadora24View,palacargadora_builder
from app.partesdiariosencargado.views import ParteEncargadoCargaView,parteEncargadoCargaView_builder,ParteEncargadoView,parteEncargadoView_builder
from app.parteoperario.views import ParteOperarioView,parteoperario_builder,CargaParteOperarioView,cargarparteoperario_builder
from app.programarcarga.views import Programarcarga, programarcarga_builder
from app.planriego.views import PlanriegoView,planriego_builder
from app.partediarioriego.views import PartediarioriegoView,partediarioriego_builder
from app.partediariolote.views import PartediarioloteView,partediariolote_builder
#R
from app.regadores.views import Regador3View, regador3_builder
from app.relacionequipos.views import relacionequipo_builder
#S
from app.separadores.views import Separador9View,separador9_builder
from app.sopbiogas.views import sopbiogas8_builder, sopbiogas8View
from app.sopdetechos.views import Sopdetecho15View, sopdetecho15_builder
from app.sustratos.views import SustratoView,sustrato_builder,mermaView,chart_merma_builder
from app.stsvs.views import StsvView,stsv_builder, stsvmasiva_builder, CargaMasivastsvView
from app.scadas.views import ScadaView, scada_builder
#T
from app.tableroelectrico.views import Tableroelectrico21View, tableroelectrico21_builder
from app.tractores.views import Tractor4View, tractores4_builder
from app.tolva.views import Tolva23, tolva23_builder
from app.transformadores.views import Transformador20View,transformador20_builder
from app.tipoagitadores.views import TipoagitadorView, tipoagitador_builder
from app.tipocamaras.views import TipocamaraView, tipocamara_builder
from app.tbombas.views import TbombaView,tbomba_builder
from app.tcaudales.views import TipocaudalView,tipocaudal_builder
from app.tconstructores.views import TipoconstruccionView,tipoconstructor_builder
from app.ttablero.views import TipotableroView, tipotablero_builder
#U
from app.unidadmedidas.views import UnidadmedidaView, unidadmedida_builder
#V
from app.vehiculos.views import Vehiculo10View, vehiculo10_builder
from app.valvdepresion.views import Valvdepresion12View, valvdepresion12_builder
from app.valvulas.views import Valtresvias25View,valvulas_builder


#from app.tipofiltros.views import TipofiltroView,tipofiltros_builder   #Tiene datos cargados por defecto
##################---------------------------------------------------##################

from . import appbuilder, db

# para limpiar permisos/vistas
# appbuilder.security_cleanup()
# db.create_all()


@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return (
        render_template(
            "404.html", base_template=appbuilder.base_template, appbuilder=appbuilder
        ),
        404,
    )





