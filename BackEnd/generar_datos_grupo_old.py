"""
Script para generar datos de prueba de un grupo de investigación en desarrollo
de aplicaciones gubernamentales (2023-2026).

Genera:
- 1 grupo de investigación
- 5-10 proyectos por año (2023-2026)
- 2-10 publicaciones por proyecto
- 2-5 participaciones en eventos por año
- Personal asociado al grupo
"""

import random
from datetime import datetime, date, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Configuración base de datos
DATABASE_URI = 'postgresql://postgres.hxrdfvfeiddvydvilrsa:Segundo_Francia_2025@aws-1-us-east-2.pooler.supabase.com:6543/postgres'

# Create engine and session
engine = create_engine(DATABASE_URI)
SessionLocal = sessionmaker(bind=engine)

# Import models after engine is created
from models.grupo import Grupo
from models.personal import Personal
from models.personaGrupo import PersonaGrupo
from models.proyecto import Proyecto
from models.equipamiento import Equipamiento
from models.bibliografia import Bibliografia
from models.gradoAcademico import GradoAcademico
from models.actividadDocente import ActividadDocente
from models.models_db import (
    Participacion, ParticipacionPersona, Institucion, 
    Distincion, Documentacion, LoginCredentials,
    Revista, Articulo, Libro,
    ProyectoLibro, ProyectoRevista, ProyectoArticulo,
    Contrato, Erogacion
)


class GeneradorDatosGrupo:
    """Generador de datos de prueba para un grupo de investigación."""
    
    def __init__(self, session):
        self.session = session
        self.grupo_id = None
        self.personas = []
        self.proyectos = []
        self.instituciones = []
        self.revistas = []
        
    def generar_todo(self):
        """Genera el set completo de datos."""
        print("🚀 Iniciando generación de datos...\n")
        
        # 1. Crear datos base (instituciones, revistas, roles)
        self.crear_datos_base()
        
        # 2. Crear grupo
        self.crear_grupo()
        
        # 3. Crear personas y asignar al grupo
        self.crear_personas()
        
        # 4. Crear proyectos por año (2023-2026)
        for year in range(2023, 2027):
            num_proyectos = random.randint(5, 10)
            print(f"📅 Año {year}: Generando {num_proyectos} proyectos...")
            for i in range(num_proyectos):
                self.crear_proyecto(year, i+1)
        
        # 5. Crear participaciones en eventos
        for year in range(2023, 2027):
            num_eventos = random.randint(2, 5)
            print(f"🎤 Año {year}: Generando {num_eventos} participaciones en eventos...")
            for i in range(num_eventos):
                self.crear_participacion_evento(year, i+1)
        
        # Commit final
        self.session.commit()
        print("\n✅ Datos generados exitosamente!")
        self.mostrar_resumen()
        
    def crear_datos_base(self):
        """Crea datos base necesarios (instituciones)."""
        print("📚 Creando datos base...")
        
        # Crear instituciones
        instituciones_data = [
            {"descripcion": "Ministerio del Interior", "pais": "Argentina"},
            {"descripcion": "Gobierno de Córdoba", "pais": "Argentina"},
            {"descripcion": "Municipalidad de Córdoba", "pais": "Argentina"},
            {"descripcion": "CONICET", "pais": "Argentina"},
            {"descripcion": "Universidad Nacional de Córdoba", "pais": "Argentina"},
        ]
        
        for inst_data in instituciones_data:
            inst = Institucion(
                descripcion=inst_data["descripcion"],
                pais=inst_data["pais"]
            )
            self.session.add(inst)
            self.instituciones.append(inst)
        
        # Flush para obtener los IDs de las instituciones
        self.session.flush()
        
        print(f"  ✓ {len(self.instituciones)} instituciones creadas")
        
    def crear_grupo(self):
        """Crea el grupo de investigación."""
        print("\n🏢 Creando grupo de investigación...")
        
        grupo = Grupo(
            sigla="GIDAG",
            nombre="Grupo de Investigación y Desarrollo de Aplicaciones Gubernamentales",
            objetivos="Desarrollar soluciones tecnológicas innovadoras para la modernización "
                      "de la gestión pública en los ámbitos nacional, provincial y municipal. "
                      "Investigar y aplicar tecnologías emergentes en e-government.",
            organigrama="Director - Subdirector - Investigadores Senior - Investigadores Junior - "
                       "Becarios - Personal de Apoyo"
        )
        self.session.add(grupo)
        self.session.flush()
        self.grupo_id = grupo.id
        print(f"  ✓ Grupo creado: {grupo.nombre} (ID: {self.grupo_id})")
        
    def crear_personas(self):
        """Crea personas y las asigna al grupo."""
        print("\n👥 Creando personal del grupo...")
        
        # Por ahora solo registramos que se deben crear
        # Las personas requieren más configuración
        print(f"  ✓ Personal se debe crear manualmente o con otro script")
        
    def crear_proyecto(self, year, numero):
        """Crea un proyecto."""
        
        # Temas de proyectos gubernamentales
        temas = [
            "Sistema de Gestión Tributaria Municipal",
            "Plataforma de Trámites Online Provinciales",
            "Portal de Transparencia Gubernamental",
            "Sistema de Firma Digital para Entes Públicos",
            "Aplicación Móvil de Atención Ciudadana",
            "Sistema de Gestión de Expedientes Electrónicos",
            "Plataforma de Participación Ciudadana",
            "Sistema de Gestión de Recursos Humanos Públicos",
            "Portal de Datos Abiertos Gubernamentales",
            "Sistema de Monitoreo de Obras Públicas",
        ]
        
        tema = random.choice(temas)
        
        # Crear proyecto
        fecha_inicio = date(year, random.randint(1, 6), random.randint(1, 28))
        duracion_meses = random.randint(12, 36)
        fecha_fin = fecha_inicio + timedelta(days=duracion_meses * 30)
        
        proyecto = Proyecto(
            codigo=f"GIDAG-{year}-{numero:02d}",
            nombre=f"{tema} {year}",
            descripcion=f"Proyecto de desarrollo de {tema.lower()} para mejorar la gestión "
                       f"y eficiencia en la administración pública.",
            tipo="Desarrollo",
            fechaInicio=fecha_inicio,
            fechaFin=fecha_fin if fecha_fin <= date(2026, 12, 31) else None,
            logros=f"Implementación exitosa de {tema.lower()} en {random.randint(5, 30)} "
                  f"municipios/provincias. Reducción del {random.randint(20, 50)}% en tiempos de gestión.",
            dificultades=f"Integración con sistemas legacy, capacitación de usuarios finales, "
                        f"resistencia al cambio en algunas áreas."
        )
        proyecto.grupoId = self.grupo_id
        self.session.add(proyecto)
        self.session.flush()
        self.proyectos.append(proyecto)
        
    def crear_participacion_evento(self, year, numero):
        """Crea una participación en evento."""
        
        # Refresh institution IDs from database to avoid stale references
        inst_query = self.session.query(Institucion).all()
        if not inst_query:
            print("    ⚠️  No hay instituciones en la base de datos!")
            return
        
        institucion = random.choice(inst_query)
        
        # Rol hardcoded ya que no tenemos RolParticipacion model
        participacion = Participacion(
            grupo=self.grupo_id,
            institucion=institucion.id,
            rol=1,  # Hardcoded ID
            personal=None
        )
        self.session.add(participacion)
        self.session.flush()
        
    def mostrar_resumen(self):
        """Muestra un resumen de los datos generados."""
        print("\n" + "="*60)
        print("📊 RESUMEN DE DATOS GENERADOS")
        print("="*60)
        print(f"Grupo: {self.grupo_id}")
        print(f"Personas: {len(self.personas)}")
        print(f"Proyectos totales: {len(self.proyectos)}")
        
        # Contar por año
        for year in range(2023, 2027):
            proyectos_year = [p for p in self.proyectos 
                            if p.fecha_inicio.year == year]
            print(f"  - Año {year}: {len(proyectos_year)} proyectos")
        
        # Contar participaciones
        num_participaciones = self.session.query(Participacion).filter(
            Participacion.grupo == self.grupo_id
        ).count()
        print(f"\nParticipaciones en eventos: {num_participaciones}")
        print("="*60)


def main():
    """Función principal."""
    session = SessionLocal()
    try:
        generador = GeneradorDatosGrupo(session)
        generador.generar_todo()
        print("\n✨ Proceso completado. Los datos están listos para consultar.")
    except Exception as e:
        session.rollback()
        print(f"\n❌ Error durante la generación: {e}")
        import traceback
        traceback.print_exc()
    finally:
        session.close()


if __name__ == '__main__':
    main()
