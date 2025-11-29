const apiUrl = "http://localhost:5000"
const equipamientoUrl = `${apiUrl}/grupo/planificacion/inventario`;


export const getEquipamiento = async () => {
    console.log('obtieniendo todo el equipamiento');
    const respuesta = await fetch(equipamientoUrl);
    if (!respuesta.ok) {
        const errorRespuesta = `No fue posible obtener el equipamiento. Código de estado: ${respuesta.status}`;
        throw new Error(errorRespuesta);
    }
    return respuesta.json();
}
