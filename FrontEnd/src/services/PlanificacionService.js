const apiUrl = "http://localhost:5000"
const planificacionUrl = `${apiUrl}/grupo/planificacion`;


export const getPlanificaciones = async () => {
    console.log('obtieniendo todas las planificaciones');
    const respuesta = await fetch(planificacionUrl);
    if (!respuesta.ok) {
        const errorRespuesta = `No fue posible obtener las planificaciones. Código de estado: ${respuesta.status}`;
        throw new Error(errorRespuesta);
    }
    return respuesta.json();
}

