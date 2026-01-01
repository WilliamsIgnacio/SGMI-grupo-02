from datetime import date
from flask import Blueprint, request, jsonify
from flask.views import MethodView
from database import db
from models.personal import Personal, Investigador, Profesional, Becario, Soporte, Visitante
from models.actividadDocente import ActividadDocente
from models.gradoAcademico import GradoAcademico
from models.models_db import Institucion, LoginCredentials
from models.enums import RolesSoporte, TipoFormacion, RolesVisitante

class AdminPersonal:

    def obtenerUnPersonal(self, id):
        return Personal.query.filter_by(id = id).first()
    
    def obtenerTodoPersonal(self):
        return Personal.query.all()
    
    def crearPersonal(self, data, operacion):

        grado = data.get('gradoAcademicoId')
        gradoObj = GradoAcademico.query.filter_by(id = grado).first()
        
        if not gradoObj:
            raise ValueError("Grado Academico no encontrado")


        #PROFESIONAL
        if operacion == 1:

            try:
                nuevoProfesional = Profesional(
                    nombre = data.get('nombre'),
                    apellido = data.get('apellido'),
                    horas = data.get('horas'),
                    gradoAcademicoId = data.get('gradoAcademicoId'),
                    institucionId = data.get('institucionId'),
                    especialidad = data.get('especialidad'),
                    descripcion = data.get('descripcion')
                )

                db.session.add(nuevoProfesional)
                db.session.commit()
                return nuevoProfesional
            
            except Exception as excepcion:
                db.session.rollback()
                raise excepcion
            

        #SOPORTE
        elif operacion == 2:
        
            rolData = data.get('rol')
            if rolData not in [rol.value for rol in RolesSoporte]:
                raise ValueError("Rol de soporte invalido")
            
            try:
                nuevoSoporte = Soporte(
                    nombre = data.get('nombre'),
                    apellido = data.get('apellido'),
                    horas = data.get('horas'),
                    gradoAcademicoId = data.get('gradoAcademicoId'),
                    institucionId = data.get('institucionId'),
                    rol = rolData
                )

                db.session.add(nuevoSoporte)
                db.session.commit()
                return nuevoSoporte
            
            except Exception as error:
                db.session.rollback()
                raise error
            
        
        #BECARIO
        elif operacion == 3:
            
            rolData = data.get('rol')

            if rolData not in [tipo.value for tipo in TipoFormacion]:
                raise ValueError("Rol de becario invalido")
            
            try:
                nuevoBecario = Becario(
                    nombre = data.get('nombre'),
                    apellido = data.get('apellido'),
                    horas = data.get('horas'),
                    gradoAcademicoId = data.get('gradoAcademicoId'),
                    institucionId = data.get('institucionId'),
                    rol = rolData
                )

                db.session.add(nuevoBecario)
                db.session.commit()
                return nuevoBecario
            
            except Exception as error:
                db.session.rollback
                raise error


        #VISITANTE
        elif operacion == 4:

            rolData = data.get('rol')

            if rolData not in [rol.value for rol in RolesVisitante]:
                raise ValueError("Rol de visitante invalido")
            
            try:
                nuevoVisitante = Visitante(
                    nombre = data.get('nombre'),
                    apellido = data.get('apellido'),
                    horas = data.get('horas'),
                    gradoAcademicoId = data.get('gradoAcademicoId'),
                    institucionId = data.get('institucionId'),
                    rol = rolData
                )

                db.session.add(nuevoVisitante)
                db.session.commit()
                return nuevoVisitante
            
            except Exception as error:
                db.session.rollback()
                raise error


        #INVESTIGADOR
        elif operacion == 5:
            
            try:
                nuevoInvestigador = Investigador(
                    nombre = data.get('nombre'),
                    apellido = data.get('apellido'),
                    horas = data.get('horas'),
                    gradoAcademicoId = data.get('gradoAcademicoId'),
                    institucionId = data.get('institucionId'),
                    categoria = data.get('categoria'),
                    incentivo = data.get('incentivo'),
                    dedicacion = data.get('dedicacion')
                )

                db.session.add(nuevoInvestigador)
                db.session.commit()
                return nuevoInvestigador
            
            except Exception as error:
                db.session.rollback()
                raise error





