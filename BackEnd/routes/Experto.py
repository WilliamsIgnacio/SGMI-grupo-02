"""
Módulo Experto de Información - Patrón Expert
Responsabilidad: Obtener y serializar datos de los modelos ORM a JSON
"""

import json
from datetime import datetime, date, time
from decimal import Decimal
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from database import db
from models.grupo import Grupo
from models.proyecto import Proyecto
from models.personaGrupo import PersonaGrupo
from models.equipamiento import Equipamiento
from models.bibliografia import Bibliografia


class ExpertoInformacion:
    """
    Patrón Expert: Centraliza la lógica de obtención y serialización de información
    de los objetos ORM. Cada modelo conoce sus atributos, y este experto sabe
    cómo extraerlos y convertirlos a formatos serializables (JSON).
    """

    def __init__(self, session: Session):
        """
        Inicializa el experto con una sesión de base de datos.
        
        Args:
            session: Sesión SQLAlchemy activa para consultas
        """
        self.session = session

    def obtener_todas_entidades(self) -> dict:
        """
        Obtiene todas las entidades de la base de datos y las devuelve como JSON.
        
        Returns:
            dict: Diccionario con todas las entidades organizadas por nombre de tabla
        """
        resultado = {}
        
        # Obtiene todos los modelos que heredan de Base
        for mapper in Base.registry.mappers:
            model_class = mapper.class_
            tabla_nombre = model_class.__tablename__
            
            try:
                # Consulta todos los registros de la tabla
                registros = self.session.query(model_class).all()
                
                # Serializa cada registro
                resultado[tabla_nombre] = [
                    self._serializar_objeto(registro) 
                    for registro in registros
                ]
            except Exception as e:
                # Si hay error en una tabla, registra el error pero continúa
                resultado[tabla_nombre] = {"error": str(e)}
        
        return resultado

    def obtener_entidad_por_tipo(self, model_class) -> dict:
        """
        Obtiene todas las instancias de un tipo de modelo específico.
        
        Args:
            model_class: La clase del modelo ORM
            
        Returns:
            dict: Diccionario con los registros serializados
        """
        tabla_nombre = model_class.__tablename__
        try:
            registros = self.session.query(model_class).all()
            return {
                tabla_nombre: [
                    self._serializar_objeto(registro) 
                    for registro in registros
                ]
            }
        except Exception as e:
            return {tabla_nombre: {"error": str(e)}}

    def obtener_por_id(self, model_class, id_valor) -> dict:
        """
        Obtiene una entidad específica por su ID.
        
        Args:
            model_class: La clase del modelo ORM
            id_valor: El valor del ID a buscar
            
        Returns:
            dict: El registro serializado o error
        """
        tabla_nombre = model_class.__tablename__
        try:
            # Intenta obtener la clave primaria
            pk_columns = inspect(model_class).primary_key
            if len(pk_columns) == 1:
                registro = self.session.query(model_class).filter(
                    pk_columns[0] == id_valor
                ).first()
                
                if registro:
                    return {tabla_nombre: self._serializar_objeto(registro)}
                else:
                    return {tabla_nombre: None}
            else:
                return {tabla_nombre: {"error": "Clave primaria compuesta no soportada"}}
        except Exception as e:
            return {tabla_nombre: {"error": str(e)}}

    def _serializar_objeto(self, objeto) -> dict:
        """
        Serializa un objeto ORM a diccionario.
        Maneja tipos especiales como datetime, date, Decimal, bytes, etc.
        
        Args:
            objeto: Instancia del modelo ORM
            
        Returns:
            dict: Representación serializable del objeto
        """
        resultado = {}
        
        # Inspecciona el mapeo del objeto para obtener sus columnas
        mapper = inspect(objeto.__class__)
        
        for columna in mapper.columns:
            nombre_columna = columna.name
            valor = getattr(objeto, nombre_columna, None)
            
            # Convierte tipos no serializables a serializables
            resultado[nombre_columna] = self._convertir_valor(valor)
        
        return resultado

    @staticmethod
    def _convertir_valor(valor):
        """
        Convierte valores no serializables a JSON-compatible.
        
        Args:
            valor: Valor a convertir
            
        Returns:
            Valor convertido a un tipo serializable
        """
        if valor is None:
            return None
        elif isinstance(valor, (str, int, float, bool)):
            return valor
        elif isinstance(valor, datetime):
            return valor.isoformat()
        elif isinstance(valor, date):
            return valor.isoformat()
        elif isinstance(valor, time):
            return valor.isoformat()
        elif isinstance(valor, Decimal):
            return float(valor)
        elif isinstance(valor, bytes):
            # Intenta decodificar como UTF-8, si no, usa hexadecimal
            try:
                return valor.decode('utf-8')
            except UnicodeDecodeError:
                return f"<binary: {valor.hex()}>"
        else:
            # Para otros tipos, intenta convertir a string
            return str(valor)

    def a_json(self, datos: dict, indent: int = 2) -> str:
        """
        Convierte un diccionario a string JSON formateado.
        
        Args:
            datos: Diccionario con los datos
            indent: Nivel de indentación (None para compacto)
            
        Returns:
            str: String JSON
        """
        return json.dumps(datos, ensure_ascii=False, indent=indent, default=str)

    def obtener_estadisticas(self) -> dict:
        """
        Obtiene estadísticas de la base de datos (conteo de registros por tabla).
        
        Returns:
            dict: Estadísticas con recuento de registros por tabla
        """
        estadisticas = {"total_tablas": 0, "total_registros": 0, "tablas": {}}
        
        for mapper in Base.registry.mappers:
            model_class = mapper.class_
            tabla_nombre = model_class.__tablename__
            
            try:
                conteo = self.session.query(model_class).count()
                estadisticas["tablas"][tabla_nombre] = conteo
                estadisticas["total_registros"] += conteo
            except Exception as e:
                estadisticas["tablas"][tabla_nombre] = {"error": str(e)}
        
        estadisticas["total_tablas"] = len(estadisticas["tablas"])
        return estadisticas

    def obtener_datos_grupo(self, id_grupo: int) -> dict:
        """
        Obtiene todos los datos relacionados con un grupo específico.
        Incluye: información del grupo, personas, proyectos, equipamiento, bibliografía.
        
        Args:
            id_grupo: ID del grupo a consultar
            
        Returns:
            dict: Datos del grupo y sus entidades relacionadas
        """
        resultado = {
            "grupo": None,
            "personas": [],
            "proyectos": [],
            "equipamiento": [],
            "bibliografia": [],
            "persona_grupo": []
        }
        
        try:
            # Obtener el grupo
            grupo = self.session.query(Grupo).filter(Grupo.id == id_grupo).first()
            if grupo:
                resultado["grupo"] = self._serializar_objeto(grupo)
            else:
                resultado["error"] = f"Grupo con ID {id_grupo} no encontrado"
                return resultado
            
            # Obtener personas asociadas al grupo (a través de PersonaGrupo)
            personas_grupos = self.session.query(PersonaGrupo).filter(
                PersonaGrupo.grupo == id_grupo
            ).all()
            
            resultado["persona_grupo"] = [
                self._serializar_objeto(pg) for pg in personas_grupos
            ]
            
            # Obtener personas
            if personas_grupos:
                from models.personal import Personal as Persona
                persona_ids = [pg.persona for pg in personas_grupos]
                personas = self.session.query(Persona).filter(
                    Persona.id.in_(persona_ids)
                ).all()
                resultado["personas"] = [
                    self._serializar_objeto(p) for p in personas
                ]
            
            # Obtener proyectos del grupo
            proyectos = self.session.query(Proyecto).filter(
                Proyecto.grupo == id_grupo
            ).all()
            resultado["proyectos"] = [
                self._serializar_objeto(p) for p in proyectos
            ]
            
            # Obtener equipamiento del grupo
            equipamiento = self.session.query(Equipamiento).filter(
                Equipamiento.grupo == id_grupo
            ).all()
            resultado["equipamiento"] = [
                self._serializar_objeto(e) for e in equipamiento
            ]
            
            # Obtener bibliografía del grupo
            bibliografia = self.session.query(Bibliografia).filter(
                Bibliografia.grupo == id_grupo
            ).all()
            resultado["bibliografia"] = [
                self._serializar_objeto(b) for b in bibliografia
            ]
            
        except Exception as e:
            resultado["error"] = str(e)
        
        return resultado

    def obtener_datos_grupo_por_fecha(self, id_grupo: int, fecha_inicio=None, 
                                      fecha_fin=None, tabla_filtro: str = None) -> dict:
        """
        Obtiene datos de un grupo específico, filtrando por rango de fechas.
        
        Args:
            id_grupo: ID del grupo
            fecha_inicio: Fecha de inicio del filtro (datetime o string YYYY-MM-DD)
            fecha_fin: Fecha de fin del filtro (datetime o string YYYY-MM-DD)
            tabla_filtro: Tabla específica a filtrar ('proyectos', 'equipamiento', 'bibliografia')
                         Si es None, filtra todas
            
        Returns:
            dict: Datos del grupo filtrados por fecha
        """
        resultado = self.obtener_datos_grupo(id_grupo)
        
        if "error" in resultado and resultado.get("grupo") is None:
            return resultado
        
        # Convertir strings a datetime si es necesario
        if isinstance(fecha_inicio, str):
            fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
        if isinstance(fecha_fin, str):
            fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
        
        try:
            # Filtrar proyectos por fecha (busca proyectos que se solapen con el rango especificado)
            if tabla_filtro is None or tabla_filtro == 'proyecto':
                proyectos_filtrados = []
                for proyecto in resultado.get("proyectos", []):
                    fecha_proj_inicio = self._parse_fecha(proyecto.get("fecha_inicio"))
                    fecha_proj_fin = self._parse_fecha(proyecto.get("fecha_fin")) if proyecto.get("fecha_fin") else None
                    
                    incluir = True
                    
                    # Un proyecto se incluye si su rango se solapa con el rango del filtro
                    # Se solapa si: inicio_proyecto <= fecha_fin Y (fin_proyecto >= fecha_inicio O fin_proyecto es None)
                    if fecha_inicio and fecha_proj_inicio:
                        # Si el proyecto termina antes de fecha_inicio, excluir
                        if fecha_proj_fin and fecha_proj_fin < fecha_inicio:
                            incluir = False
                    
                    if incluir and fecha_fin and fecha_proj_inicio:
                        # Si el proyecto comienza después de fecha_fin, excluir
                        if fecha_proj_inicio > fecha_fin:
                            incluir = False
                    
                    if incluir:
                        proyectos_filtrados.append(proyecto)
                
                resultado["proyectos"] = proyectos_filtrados
            
            # Filtrar equipamiento por fecha (fecha_incorporacion)
            if tabla_filtro is None or tabla_filtro == 'equipamiento':
                equipamiento_filtrado = []
                for equipo in resultado.get("equipamiento", []):
                    incluir = True
                    
                    if fecha_inicio and "fecha_incorporacion" in equipo:
                        fecha_equipo = self._parse_fecha(equipo["fecha_incorporacion"])
                        if fecha_equipo and fecha_equipo < fecha_inicio:
                            incluir = False
                    
                    if incluir and fecha_fin and "fecha_incorporacion" in equipo:
                        fecha_equipo = self._parse_fecha(equipo["fecha_incorporacion"])
                        if fecha_equipo and fecha_equipo > fecha_fin:
                            incluir = False
                    
                    if incluir:
                        equipamiento_filtrado.append(equipo)
                
                resultado["equipamiento"] = equipamiento_filtrado
            
            # Filtrar bibliografía por fecha (año_publicacion o fecha)
            if tabla_filtro is None or tabla_filtro == 'bibliografia':
                bibliografia_filtrada = []
                for bib in resultado.get("bibliografia", []):
                    incluir = True
                    
                    # Buscar campos de fecha en bibliografía
                    for campo_fecha in ["fecha", "ano_publicacion", "año_publicacion"]:
                        if campo_fecha in bib:
                            valor = bib[campo_fecha]
                            if isinstance(valor, int):
                                valor = date(valor, 1, 1)
                            else:
                                valor = self._parse_fecha(valor)
                            
                            if valor and fecha_inicio and valor < fecha_inicio:
                                incluir = False
                            if incluir and valor and fecha_fin and valor > fecha_fin:
                                incluir = False
                            break
                    
                    if incluir:
                        bibliografia_filtrada.append(bib)
                
                resultado["bibliografia"] = bibliografia_filtrada
            
            resultado["filtros_aplicados"] = {
                "fecha_inicio": fecha_inicio.isoformat() if fecha_inicio else None,
                "fecha_fin": fecha_fin.isoformat() if fecha_fin else None,
                "tabla_filtro": tabla_filtro
            }
            
        except Exception as e:
            resultado["error_filtrado"] = str(e)
        
        return resultado

    def _parse_fecha(self, valor) -> date:
        """
        Intenta parsear una fecha desde diferentes formatos.
        
        Args:
            valor: Valor a parsear (string, date, datetime)
            
        Returns:
            date: Fecha parseada o None si no se puede parsear
        """
        if valor is None:
            return None
        
        if isinstance(valor, date):
            return valor
        
        if isinstance(valor, datetime):
            return valor.date()
        
        if isinstance(valor, str):
            # Intentar diferentes formatos
            formatos = [
                '%Y-%m-%d',
                '%d-%m-%Y',
                '%Y/%m/%d',
                '%d/%m/%Y',
            ]
            for fmt in formatos:
                try:
                    return datetime.strptime(valor, fmt).date()
                except ValueError:
                    continue
        
        return None
