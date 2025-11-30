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

class RolGrupo(enum.Enum):
    MIEMBRO = "miembro"
    DIRECTOR = "director"
    COORDINADOR = "coordinador"
    INVESTIGADOR_PRINCIPAL = "investigadorPrincipal"
    COLABORADOR = "colaborador"

class RolParticipacion(enum.Enum):
    JURADO = "Jurado"
    EVALUADOR = "Evaluador"
    PANELISTA = "Panelista"
    MIEMBROCOMITE = "Miembro de Comité"
    

class TipoContrato(enum.Enum):
    TRANSFERENCIATECNOLOGIA = "Contrato de Transferencia de Tecnologia"
    IDI = "Contrato I+D+i"
    TRANSFERENCIACONOCIMIENTO = "Contrato de Transferencia de Conocimiento"
    ASISTENCIATECNICA = "Contrato de Asistencia Técnica"
    SUPERVISION = "Contrato de Supervisión y Ensayos de Laboratorio"
    DIFUSIONA = "Difusión a la Comunidad Académica y General"

class TipoErogacion(enum.Enum):
    CORRIENTE = "Corriente"
    CAPITAL = "De Capital"
