const apiUrl = "http://localhost:5000"
const bibliografiaUrl = `${apiUrl}/grupo/planificacion/inventario`;


export const getBibliografia = async () => {
    console.log('obtieniendo todo la bibliografia');
    const respuesta = await fetch(bibliografiaUrl);
    if (!respuesta.ok) {
        const errorRespuesta = `No fue posible obtener la bibliografia. Código de estado: ${respuesta.status}`;
        throw new Error(errorRespuesta);
    }
    return respuesta.json();
}


