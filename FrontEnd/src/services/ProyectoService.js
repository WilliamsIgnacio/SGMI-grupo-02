const apiUrl = "http://localhost:5000"
const proyectoUrl = `${apiUrl}/api/proyecto`;


export const getProyectos = async () => {
    console.log('obtieniendo todas las planificaciones');
    const respuesta = await fetch(proyectoUrl);
    if (!respuesta.ok) {
        const errorRespuesta = `No fue posible obtener las planificaciones. Código de estado: ${respuesta.status}`;
        throw new Error(errorRespuesta);
    }
    return respuesta.json();
}

export const createProyecto = async (proyectoData) => {
    const response = await fetch(proyectoUrl, {
        method: 'POST',
        body: JSON.stringify(proyectoData),
    });
    if (!response.ok) {
        throw new Error('No se pudo crear el proyecto');
    }
    return response.json();
};

/*
JSON
{
  "codigo": "P-001",
  "nombre": "Proyecto IA",
  "descripcion": "...",
  "tipo": "I+D",
  "logros": "...",
  "dificultades": "...",
  "fechaInicio": "2024-01-01",
  "fechaFin": "2025-01-01",
  "grupoId": 5
}

*/

export const updateProyecto = async (id, proyectoData) => {
    const response = await fetch(`${proyectoUrl}/${id}`, {
        method: 'PUT',
        body: JSON.stringify(proyectoData),
    });
    if (!response.ok) {
        throw new Error('No se pudo actualizar el proyecto');
    }
    return response.json();
};

export const deleteProyecto = async (id) => {
    const response = await fetch(`${proyectoUrl}/${id}`, {
        method: 'DELETE',
    });
    if (!response.ok) {
        throw new Error('No se pudo eliminar el proyecto');
    }
    return response.json();
};