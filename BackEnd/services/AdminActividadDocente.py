from datetime import datetime
from models.actividadDocente import ActividadDocente
from database import db

class AdminActividadDocente:
    @staticmethod

    def convertir_fecha(fecha_texto):
        if not fecha_texto:
            return None
        try:
            return datetime.strptime(fecha_texto, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            return None
        

    def obtener_todas(self):
        return ActividadDocente.all()
    

    def obtener_por_id(self, id):
        return ActividadDocente.query.get(id)
    
    
    def crear(self, data):
        if not data.get('personalId') or not data.get('institucionId'):
            raise ValueError('Faltan campos obligatorios (personalId, institucionId)')
        
        nueva_actividad = ActividadDocente(
            fechaInicio = self.convertir_fecha(data.get('fechaInicio')),
            fechaFin = self.convertir_fecha(data.get('fechaFin')),
            rol = data.get('rol'),
            personalId = data.get('personalId'),
            institucionId = data.get('institucionId')
        )

        db.session.add(nueva_actividad)
        db.session.commit()
        return nueva_actividad


    def modificar(self, id, data):
        actividad = ActividadDocente.query.get(id)

        if not actividad:
            raise ValueError('Actividad Docente no encontrada')
        
        if 'fechaInicio' in data:
            actividad.fechaInicio = self.convertir_fecha(data.get('fechaInicio'))
        
        if 'fechaFin' in data:
            actividad.fechaFin = self.convertir_fecha(data.get('fechaFin'))
        
        actividad.rol = data.get('rol', actividad.rol)
        actividad.personalId = data.get('personalId', actividad.personalId)
        actividad.institucionId = data.get('institucionId', actividad.institucionId)

        db.session.commit()
        return actividad
    

    def eliminar(self, id):
        actividad = ActividadDocente.query.get(id)
        if not actividad:
            return False
        db.session.delete(actividad)
        db.session.commit()
        return True