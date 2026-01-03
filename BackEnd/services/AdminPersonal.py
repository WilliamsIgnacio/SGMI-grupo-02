from datetime import date, datetime
from database import db
from models.personal import Personal, Investigador, Profesional, Becario, Soporte, Visitante
from models.personaGrupo import PersonaGrupo
from models.gradoAcademico import GradoAcademico
from models.enums import RolesSoporte, TipoFormacion, RolesVisitante
from services.AdminGrupo import AdminGrupo

administradorGrupo = AdminGrupo()

class AdminPersonal:

    def obtenerUnPersonal(self, id):
        return Personal.query.filter_by(id = id).first()
    

    def obtenerTodoPersonal(self):
        return Personal.query.all()
    
    def obtenerPersonalDeGrupo(self, grupo):
        return 
    

    def vincularPersonaGrupo(self, data, personaId):
        #Crear vinculo con grupo
        
        fechaInicio = datetime.strptime(data.get('fechaInicio'), '%d-%m-%Y').date()
        fechaFin = data.get('fechaFin')
        
        if fechaFin:
            fechaFin = datetime.strptime(fechaFin, '%d-%m-%Y').date()
        else:
            fechaFin = None

        grupo = data.get('grupoId')

        existeGrupo = administradorGrupo.obtenerUnGrupo(grupo)
        if not existeGrupo:
            raise ValueError('El grupo no existe')
        
        existePersonal = self.obtenerUnPersonal(personaId)
        if not existePersonal:
            raise ValueError('No se encontro el personal')
        

        try:

            relacionPersonaGrupo = PersonaGrupo(
                grupo = grupo,
                persona = personaId,
                fecha_inicio = fechaInicio,
                fecha_fin = fechaFin
            )

            db.session.add(relacionPersonaGrupo)
            db.session.commit()

            return relacionPersonaGrupo

        except Exception as excepcion:
                db.session.rollback()
                print(f"Error en vinculación: {str(excepcion)}")
                raise excepcion
        

    def crearPersonal(self, data, operacion):

        personal = data.get('personal')
        grado = personal.get('gradoAcademicoId')

        gradoObj = GradoAcademico.query.filter_by(id = grado).first()
        
        if not gradoObj:
            raise ValueError("Grado Academico no encontrado")


        #PROFESIONAL
        if operacion == 1:

            try:
                nuevoProfesional = Profesional(
                    nombre = personal.get('nombre'),
                    apellido = personal.get('apellido'),
                    horas = personal.get('horas'),
                    gradoAcademicoId = personal.get('gradoAcademicoId'),
                    institucionId = personal.get('institucionId'),
                    especialidad = personal.get('especialidad'),
                    descripcion = personal.get('descripcion')
                )

                db.session.add(nuevoProfesional)
                db.session.commit()

                personaGrupo = self.vincularPersonaGrupo(data, nuevoProfesional.id)

                return personaGrupo
            
            except Exception as excepcion:
                db.session.rollback()
                raise excepcion
            

        #SOPORTE
        elif operacion == 2:
        
            rolpersonal = personal.get('rol')
            if rolpersonal not in [rol.value for rol in RolesSoporte]:
                raise ValueError("Rol de soporte invalido")
            
            try:
                nuevoSoporte = Soporte(
                    nombre = personal.get('nombre'),
                    apellido = personal.get('apellido'),
                    horas = personal.get('horas'),
                    gradoAcademicoId = personal.get('gradoAcademicoId'),
                    institucionId = personal.get('institucionId'),
                    rol = rolpersonal
                )

                db.session.add(nuevoSoporte)
                db.session.commit()
                
                personaGrupo = self.vincularPersonaGrupo(data, nuevoSoporte.id)

                return personaGrupo
            
            except Exception as error:
                db.session.rollback()
                raise error
            
        
        #BECARIO
        elif operacion == 3:
            
            rolpersonal = personal.get('rol')

            if rolpersonal not in [tipo.value for tipo in TipoFormacion]:
                raise ValueError("Rol de becario invalido")
            
            try:
                nuevoBecario = Becario(
                    nombre = personal.get('nombre'),
                    apellido = personal.get('apellido'),
                    horas = personal.get('horas'),
                    gradoAcademicoId = personal.get('gradoAcademicoId'),
                    institucionId = personal.get('institucionId'),
                    rol = rolpersonal
                )

                db.session.add(nuevoBecario)
                db.session.commit()
                
                personaGrupo = self.vincularPersonaGrupo(data, nuevoBecario.id)

                return personaGrupo
            
            except Exception as error:
                db.session.rollback
                raise error


        #VISITANTE
        elif operacion == 4:

            rolpersonal = personal.get('rol')

            if rolpersonal not in [rol.value for rol in RolesVisitante]:
                raise ValueError("Rol de visitante invalido")
            
            try:
                nuevoVisitante = Visitante(
                    nombre = personal.get('nombre'),
                    apellido = personal.get('apellido'),
                    horas = personal.get('horas'),
                    gradoAcademicoId = personal.get('gradoAcademicoId'),
                    institucionId = personal.get('institucionId'),
                    rol = rolpersonal
                )

                db.session.add(nuevoVisitante)
                db.session.commit()
                
                personaGrupo = self.vincularPersonaGrupo(data, nuevoVisitante.id)

                return personaGrupo
            
            except Exception as error:
                db.session.rollback()
                raise error


        #INVESTIGADOR
        elif operacion == 5:
            
            try:
                nuevoInvestigador = Investigador(
                    nombre = personal.get('nombre'),
                    apellido = personal.get('apellido'),
                    horas = personal.get('horas'),
                    gradoAcademicoId = personal.get('gradoAcademicoId'),
                    institucionId = personal.get('institucionId'),
                    categoria = personal.get('categoria'),
                    incentivo = personal.get('incentivo'),
                    dedicacion = personal.get('dedicacion')
                )

                db.session.add(nuevoInvestigador)
                db.session.commit()
                
                personaGrupo = self.vincularPersonaGrupo(data, nuevoInvestigador.id)

                return personaGrupo
            
            except Exception as error:
                db.session.rollback()
                raise error


        



