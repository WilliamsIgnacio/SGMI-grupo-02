from flask import Flask, jsonify
from flask_cors import CORS
from database import db

app = Flask(__name__)
CORS(app) 

#configuracion base de datos
DATABASE_URI = 'postgresql://postgres.hxrdfvfeiddvydvilrsa:Segundo_Francia_2025@aws-1-us-east-2.pooler.supabase.com:6543/postgres'

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

from models.actividadDocente import ActividadDocente
from models.gradoAcademico import GradoAcademico
from models.personal import Personal, Becario, Investigador, Profesional, Soporte, Visitante
from models.proyecto import Proyecto

from routes.controladorBecario import becario_bp
from routes.controladorInvestigador import investigador_bp
from routes.controladorProfesional import profesional_bp
from routes.controladorSoporte import soporte_bp
from routes.controladorVisitante import visitante_bp
from routes.controladorProyecto import proyecto_bp
from routes.controladorGradoAcademico import grado_academico_bp
from routes.controladorActividadDocente import actividad_docente_bp


#configuracion apis
app.register_blueprint(becario_bp, url_prefix='/api/becarios')
app.register_blueprint(investigador_bp, url_prefix='/api/investigadores')
app.register_blueprint(profesional_bp, url_prefix='/api/profesionales')
app.register_blueprint(soporte_bp, url_prefix='/api/soportes')
app.register_blueprint(visitante_bp, url_prefix='/api/visitantes')
app.register_blueprint(proyecto_bp, url_prefix='/api/proyectos')
app.register_blueprint(grado_academico_bp, url_prefix='/api/grados-academicos')
app.register_blueprint(actividad_docente_bp, url_prefix='/api/actividades-docente')


#Prueba para ver que todo este instalado correctamente
@app.route("/api/hello")
def get_hello():
    return jsonify({"message": "ESTO ES UNA PRUEBA"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)