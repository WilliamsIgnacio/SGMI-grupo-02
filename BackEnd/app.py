from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy


from routes.controladorBecario import becario_bp
from routes.controladorInvestigador import investigador_bp
from routes.controladorProfesional import profesional_bp
from routes.controladorSoporte import soporte_bp
from routes.controladorVisitante import visitante_bp
from routes.controladorProyecto import proyecto_bp
#Prueba para ver que todo este instalado correctamente

app = Flask(__name__)
CORS(app) 

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///proyecto.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
app.register_blueprint(becario_bp, url_prefix='/api/becarios')
app.register_blueprint(investigador_bp, url_prefix='/api/investigadores')
app.register_blueprint(profesional_bp, url_prefix='/api/profesionales')
app.register_blueprint(soporte_bp, url_prefix='/api/soportes')
app.register_blueprint(visitante_bp, url_prefix='/api/visitantes')
app.register_blueprint(proyecto_bp, url_prefix='/api/proyectos')


@app.route("/api/hello")
def get_hello():
    return jsonify({"message": "ESTO ES UNA PRUEBA"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)