const apiUrl = "http://localhost:5000"
const personalUrl = `${apiUrl}/grupo/planificacion/personal`;


export const getPersonal = async () => {
    console.log('obtieniendo todo el personal');
    const respuesta = await fetch(personalUrl);
    if (!respuesta.ok) {
        const errorRespuesta = `No fue posible obtener el personal. Código de estado: ${respuesta.status}`;
        throw new Error(errorRespuesta);
    }
    return respuesta.json();
}
