const apiUrl = "http://localhost:5000"
const grupoUrl = `${apiUrl}/grupo`;


export const getGrupos = async () => {
    console.log('obtieniendo todos los grupos');
    const respuesta = await fetch(grupoUrl);
    if (!respuesta.ok) {
        const errorRespuesta = `No fue posible obtener los grupos. Código de estado: ${respuesta.status}`;
        throw new Error(errorRespuesta);
    }
    return respuesta.json();
}

