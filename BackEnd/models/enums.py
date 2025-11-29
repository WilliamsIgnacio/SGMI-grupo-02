import enum

class RolesSoporte(enum.Enum):
    TECNICO = "tecnico"
    APOYO = "apoyo"
    ADMINISTRATIVO = "administrativo"

class RolesVisitante(enum.Enum):
    ACADEMICA = "academica"
    TECNICA = "tecnica"

class TipoFormacion(enum.Enum):
    DOCTORADO = "doctorado"
    MAESTRIA = "maestria/especializacion"
    BECARIO_GRADUADO = "becarioGraduado"
    BECARIO_ALUMNO = "becarioAlumno"
    PASANTE = "pasante"
    PROYECTO_FINAL = "proyectoFinal/TesisDePosgrado"