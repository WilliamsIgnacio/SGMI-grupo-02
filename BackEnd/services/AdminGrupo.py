from datetime import date
from sqlalchemy.exc import IntegrityError
from flask import Blueprint, request, jsonify
from flask.views import MethodView

#MODELOS
from database import db
from models.grupo import Grupo


class AdminGrupo(MethodView):

    def obtenerUnGrupo(self, id):
        return Grupo.query.filter_by(id = id).first()
    

    def obtenerTodosGrupos(self):
        return Grupo.query.all()
    

    def crearGrupo(self, grupo):

        try:
            nuevoGrupo = Grupo(
                sigla = grupo.get('sigla'),
                nombre = grupo.get('nombre'),
                objetivos = grupo.get('objetivos'),
                organigrama = grupo.get('organigrama'),
                correo_electronico = grupo.get('correo_electronico'),
                director = grupo.get('director'),
                vicedirector = grupo.get('vicedirector'),
                consejo_ejecutivo = grupo.get('consejo_ejecutivo'),
                unidad_academica = grupo.get('unidad_academica'),
                activo = grupo.get('activo'),
            )

            db.session.add(nuevoGrupo)
            db.session.commit()

            return nuevoGrupo
        
        except Exception as excepcion:
                db.session.rollback()
                raise excepcion
        
    
    def modificarGrupo(self, data, idGrupo):

        try:
            grupoSeleccionado = Grupo.query.filter_by(id = idGrupo).first()

            if not grupoSeleccionado:
                respuesta = jsonify({'mensaje': 'Grupo no encontrado'}) 
                return respuesta
            
            camposPermitidos = ['sigla', 'nombre', 'objetivos', 'organigrama', 'correo_electronico', 'director', 'vicedirector', 'consejo_ejecutivo', 'unidad_academica']

            for campo in camposPermitidos:
                if campo in data:
                    setattr(grupoSeleccionado, campo, data[campo])

            db.session.commit()
            return grupoSeleccionado
    
        except Exception as excepcion:
            db.session.rollback()
            raise excepcion