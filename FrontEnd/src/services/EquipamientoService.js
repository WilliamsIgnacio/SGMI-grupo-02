const apiUrl = "http://localhost:5000"
const equipamientoUrl = `${apiUrl}/api/inventario`;


export const getEquipamiento = async (idGrupo) => {
    console.log('obtieniendo todo el equipamiento');
    const respuesta = await fetch({equipamientoUrl}/{idGrupo});
    if (!respuesta.ok) {
        const errorRespuesta = `No fue posible obtener el equipamiento. Código de estado: ${respuesta.status}`;
        throw new Error(errorRespuesta);
    }
    return respuesta.json();
}

export const createEquipamiento = async (equipamientoData) => {
    const response = await fetch(equipamientoUrl, {
        method: 'POST',
        body: JSON.stringify(equipamientoData),
    });
    if (!response.ok) {
        throw new Error('No se pudo crear el proyecto');
    }
    return response.json();
};

/*
JSON
{
  "denominacion": "Servidor Dell",
  "fecha_ingreso": "2023-05-20",
  "monto": 1500.00,
  "grupo": 5,
  "descripcion": "Servidor principal"
}
*/

export const deleteEquipamiento = async (id) => {
    const response = await fetch(`${equipamientoUrl}/${id}`, {
        method: 'DELETE',
    });
    if (!response.ok) {
        throw new Error('No se pudo eliminar el equipamiento');
    }
    return response.json();
};

export const getEstadisticasEquipamiento = async (idGrupo) => {
    console.log('obtieniendo todo el equipamiento');
    const respuesta = await fetch(`${equipamientoUrl}/grupo/${idGrupo}`);
    if (!respuesta.ok) {
        const errorRespuesta = `No fue posible obtener las estadisticas del equipamiento. Código de estado: ${respuesta.status}`;
        throw new Error(errorRespuesta);
    }
    return respuesta.json();
}