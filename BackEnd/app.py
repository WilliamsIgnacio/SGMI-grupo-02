from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

#Prueba para ver que todo este instalado correctamente

app = Flask(__name__)
CORS(app) 

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///proyecto.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


@app.route("/api/hello")
def get_hello():
    return jsonify({"message": "ESTO ES UNA PRUEBA"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)