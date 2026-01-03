import os
from dotenv import load_dotenv

from flask import Flask, jsonify
from flask_cors import CORS
from database import db

app = Flask(__name__)
CORS(app) 

# Cargar variables de entorno del archivo .env
load_dotenv()

#configuracion base de datos
DATABASE_URI = os.getenv('DATABASE_URL')

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# ============ Import Models ============
from models.actividadDocente import ActividadDocente
# from models.enums import RolGrupo, RolParticipacion, TipoContrato, TipoErogacion
from models.bibliografia import Bibliografia
from models.equipamiento import Equipamiento
from models.gradoAcademico import GradoAcademico
from models.grupo import Grupo
from models.models_db import (
    Institucion, Documentacion, LoginCredentials,
    Revista, Articulo, Libro,
    ProyectoLibro, ProyectoRevista, ProyectoArticulo,
    Contrato, Participacion, ParticipacionPersona,
    Distincion, Erogacion
)
from models.personaGrupo import PersonaGrupo
from models.personal import Personal, Becario, Investigador, Profesional, Soporte, Visitante
from models.proyecto import Proyecto

# ============ Import Routes ============
from routes.controladorActividadDocente import actividad_docente_bp
from routes.controladorEnumerativas import enums_bp
from routes.controladorExperto import experto_bp
from routes.controladorGradoAcademico import grado_academico_bp
from routes.ControladorInventario import inventario_bp
from routes.ControladorParticipacion import participacion_bp
from routes.ControladorPersonal import personal_bp
from routes.controladorProyecto import proyecto_bp
from routes.ControladorGrupo import grupos_bp

# ============ Register Blueprints ============
app.register_blueprint(actividad_docente_bp, url_prefix='/api/actividades-docente')  #Funciona todo
app.register_blueprint(enums_bp, url_prefix='/api/enums')
app.register_blueprint(experto_bp)
app.register_blueprint(grado_academico_bp, url_prefix='/api/grados-academicos')
app.register_blueprint(inventario_bp)
app.register_blueprint(grupos_bp, url_prefix='/api/grupos')
app.register_blueprint(participacion_bp)
app.register_blueprint(personal_bp, url_prefix='/api/personal')
app.register_blueprint(proyecto_bp, url_prefix='/api/proyectos')


#Prueba para ver que todo este instalado correctamente
@app.route("/api/hello")
def get_hello():
    return jsonify({"message": "ESTO ES UNA PRUEBA"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
    