const apiUrl = "http://localhost:5000"
const grupoUrl = `${apiUrl}/api/organizaciones`;


export const getGrupos = async () => {
    console.log('obtieniendo todos los grupos');
    const respuesta = await fetch(grupoUrl);
    if (!respuesta.ok) {
        const errorRespuesta = `No fue posible obtener los grupos. Código de estado: ${respuesta.status}`;
        throw new Error(errorRespuesta);
    }
    return respuesta.json();
}

export const getGrupo = async (id) => {
    console.log('obteniendo un solo grupo');
    const respuesta = await fetch({grupoUrl}/{id});
    if (!respuesta.ok) {
        const errorRespuesta = `No fue posible obtener los grupos. Código de estado: ${respuesta.status}`;
        throw new Error(errorRespuesta);
    }
    return respuesta.json();
}

export const createGrupo = async (grupoData) => {
    const response = await fetch(grupoUrl, {
        method: 'POST',
        body: JSON.stringify(grupoData),
    });
    if (!response.ok) {
        throw new Error('No se pudo crear el grupo');
    }
    return response.json();
};

export const updateGrupo = async (id, grupoData) => {
    const response = await fetch(`${grupoUrl}/${id}`, {
        method: 'PUT',
        body: JSON.stringify(grupoData),
    });
    if (!response.ok) {
        throw new Error('No se pudo actualizar el grupo');
    }
    return response.json();
};

export const deleteGrupo = async (id,) => {
    const response = await fetch(`${grupoUrl}/${id}`, {
        method: 'DELETE',
    });
    if (!response.ok) {
        throw new Error('No se pudo eliminar el grupo');
    }
    return response.json();
};