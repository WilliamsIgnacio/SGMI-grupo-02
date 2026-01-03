import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom"
import "./Grupo.css";

import Tabla from "../../components/Tabla";
import Boton from "../../components/Boton";
import BotonAgregar from "../../components/BotonAgregar";
import imagenMas from "../../images/mas.png";
import imagenEliminar from "../../images/eliminar.png"
import imagenModificar from "../../images/modificar.png"
import FormularioGrupo from "./FormularioGrupo"; 

import { getGrupos, getGrupo, createGrupo, updateGrupo, deleteGrupo } from "../../services/GrupoService";


import ModalFormularios from "../../components/ModalFormularios";
import FloatingLabel from 'react-bootstrap/FloatingLabel';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';
import Pagination from 'react-bootstrap/Pagination'; 


const itemsPorPagina = 5;

function Grupo() {
    const navegar = useNavigate(); 

    const [mostrarModal, setMostrarModal] = useState(false); 
    
    const [grupos, setGrupos] = useState([]);
    
    let tamanio = grupos.length;
    
    const [paginaActual, setPaginaActual] = useState(1); 
    
    const [grupoSeleccionadoId, setGrupoSeleccionadoId] = useState(null); 
    
    const [infoModal, setInfoModal] = useState({ 
        titulo: '',
        tipo: null 
    });

    const [datosNuevoGrupo, setDatosNuevoGrupo] = useState({ 
        sigla: '', 
        nombre: '', 
        unidad_academica: '',
        director: '', 
        vicedirector: '', 
        correoElectronico: '',
        objetivos: '',
        organigrama: '',
        consejo_ejecutivo: ''
    });
    
    const [datosFormularioGrupo, setDatosFormularioGrupo] = useState({ 
        sigla: '', 
        nombre: '', 
        unidad_academica: '',
        director: '', 
        vicedirector: '', 
        correoElectronico: '',
        objetivos: '',
        organigrama: '',
        consejo_ejecutivo: ''
    });

    const [contenidoDetalle, setContenidoDetalle] = useState({ 
        campo: null, 
        contenido: '', 
        grupoId: null,
    });
    
    const [idGrupoAModificar, setIdGrupoAModificar] = useState(null); 

    const [claveFormulario, setClaveFormulario] = useState(0); 
    
    const columnas = [
        "Selección", 
        "Sigla", 
        "Nombre", 
        "Unidad Academica", 
        "Director/a", 
        "Vicedirector/a", 
        "Correo Electronico", 
        "Acciones"
    ];

    const handleCambioRadio = (id) => { 
        setGrupoSeleccionadoId(id);
    };

    useEffect(() => {
        obtenerGrupos(); 
    }, []);

    const obtenerGrupos = async () => {
        try {
            const data = await getGrupos();
            setGrupos(data.reverse());
            setPaginaActual(1); 
        } catch (error) {
            console.error("Error al obtener los grupos:", error);
        }
    };

    const handleFormularioNuevo = (error) => { 
        const { name, value } = error.target; 
        setDatosNuevoGrupo(prev => ({ ...prev, [name]: value }));
    }

    const handleCambioFormularioExistente = (error) => { 
        const { name, value } = error.target;
        setDatosFormularioGrupo(prevData => ({ ...prevData, [name]: value }));
    };

    const handleEnvio = async (error) => { 
        error.preventDefault(); 
        try {
            const datosACrear = {
                ...datosNuevoGrupo,
                //objetivos: datosNuevoGrupo.objetivos || '',
                //organigrama: datosNuevoGrupo.organigrama || ''
                consejo_ejecutivo: datosNuevoGrupo.consejo_ejecutivo || ''    
            };

            await createGrupo(datosACrear);
            setDatosNuevoGrupo({ sigla: '', nombre: '', unidad_academica: '', director: '', vicedirector: '', correoElectronico: '', objetivos: '', organigrama: '' });
            await obtenerGrupos(); 
            setMostrarModal(false); 
        } catch (error) {
            console.error("Error al crear el grupo:", error);
            alert(`Error al crear el grupo: ${error.message}`);
        }
    };

    const handleActualizacion = async (error) => { 
        error.preventDefault();
        if (!idGrupoAModificar) return console.error("No hay ID de grupo para actualizar.");

        try {
            await updateGrupo(idGrupoAModificar, datosFormularioGrupo);
            await obtenerGrupos(); 
            setIdGrupoAModificar(null);
            setDatosFormularioGrupo({ sigla: '', nombre: '', unidad_academica: '', director: '', vicedirector: '', correoElectronico: '' });
            setMostrarModal(false); 
        } catch (error) {
            console.error("Error al modificar el grupo:", error);
            alert(`Error al modificar el grupo: ${error.message}`);
        }
    };
    
    const iniciarModificacion = async (id) => {
        try {
            const grupoAModificar = await getGrupo(id);
            setIdGrupoAModificar(id); 
            
            setDatosFormularioGrupo({
                sigla: grupoAModificar.sigla || '',
                nombre: grupoAModificar.nombre || '',
                unidad_academica: grupoAModificar.unidad_academica || '',
                director: grupoAModificar.director || '',
                vicedirector: grupoAModificar.vicedirector || '',
                correoElectronico: grupoAModificar.correoElectronico || '',
            });

            setInfoModal({
                titulo: `Modificar Grupo: ${grupoAModificar.nombre}`,
                tipo: 'modificar'
            });
            setMostrarModal(true);

        } catch (error) {
            console.error("Error al cargar datos para modificar:", error);
            alert(`No se pudo cargar el grupo para edición: ${error.message}`); 
        }
    };
    
    const handleEliminacion = async (id, nombre) => { 
        const confirmar = window.confirm(`¿Estás seguro de que deseas eliminar el grupo "${nombre}"? Esta acción es irreversible.`);
        
        if (confirmar) {
            try {
                await deleteGrupo(id); 
                alert(`El grupo "${nombre}" ha sido eliminado exitosamente.`);
                await obtenerGrupos(); 
                
            } catch (error) {
                console.error("Error al eliminar el grupo:", error);
                alert(`No se pudo eliminar el grupo "${nombre}": ${error.message}`);
            }
        }
    };

    const obtenerYAbrirModalDetalle = (campoUI, tituloModal) => { 
        if (!grupoSeleccionadoId) {
            alert("Por favor, selecciona un grupo primero.");
            return;
        }
        
        let campoJSON;
        if (campoUI === 'objetivo') {
            campoJSON = 'objetivos';
        } else if (campoUI === 'consejoEjecutivo') {
            campoJSON = 'consejo_ejecutivo';
        } else if (campoUI === 'organigrama') {
            campoJSON = 'organigrama';
        } else {
            console.error("Campo de detalle no válido:", campoUI);
            return;
        }

        const grupoSeleccionado = grupos.find(g => g.id === grupoSeleccionadoId);
        if (!grupoSeleccionado) {
            alert("Error: No se encontró el grupo seleccionado en los datos.");
            return;
        }

        const contenido = grupoSeleccionado[campoJSON] || "";
        
        setContenidoDetalle({
            campo: campoJSON, 
            contenido: contenido,
            grupoId: grupoSeleccionadoId,
        });
        setInfoModal({ titulo: tituloModal, tipo: 'verDetalle' });
        setMostrarModal(true);
    };

    function verObjetivos() {
        obtenerYAbrirModalDetalle('objetivo', 'Objetivos del Grupo');
    }

    function verOrganigrama() {
        obtenerYAbrirModalDetalle('organigrama', 'Organigrama del Grupo');
    }

    function verConsejoEjecutivo() {
        obtenerYAbrirModalDetalle('consejoEjecutivo', 'Consejo Ejecutivo');
    }

    const iniciarEdicionDetalle = () => { 
        setInfoModal(prev => ({ ...prev, tipo: 'modificarDetalle' }));
    };

    const manejarCambioDetalle = (e) => { 
        setContenidoDetalle(prev => ({ ...prev, contenido: e.target.value }));
    };

    const handleEnvioDetalle = async (e) => { 
        e.preventDefault();
        const { grupoId, campo, contenido } = contenidoDetalle;

        if (!grupoId || !campo) {
            alert("Error: Grupo o campo no definido para guardar.");
            return;
        }

        try {
            const grupoActual = grupos.find(g => g.id === grupoId);
            
            if (!grupoActual) {
                throw new Error("Grupo no encontrado para actualizar.");
            }
            
            const datosActualizados = {
                ...grupoActual,
                [campo]: contenido, 
            };

            await updateGrupo(grupoId, datosActualizados); 
            
            alert(`${infoModal.titulo} actualizado exitosamente.`);
            setMostrarModal(false);

            await obtenerGrupos(); 

        } catch (error) {
            console.error(`Error al actualizar ${campo}:`, error);
            alert(`Error al actualizar ${infoModal.titulo}: ${error.message}`);
        }
    };

    function agregarGrupo(){
        setDatosNuevoGrupo({ sigla: '', nombre: '', unidad_academica: '', director: '', vicedirector: '', correoElectronico: '' });
        setIdGrupoAModificar(null); 
        setClaveFormulario(prevKey => prevKey + 1);
        setInfoModal({ titulo: "Agregar Grupo", tipo: 'agregar' });
        setMostrarModal(true);
    }

    function verPlanificacion(){
        navegar("planificacion");
    }
    

    const indiceUltimoItem = paginaActual * itemsPorPagina; 
    const indicePrimerItem = indiceUltimoItem - itemsPorPagina;
    
    const gruposActuales = grupos.slice(indicePrimerItem, indiceUltimoItem);
    
    const totalPaginas = Math.ceil(grupos.length / itemsPorPagina); 

    const paginar = (numeroPagina) => { // paginate -> paginar
        setPaginaActual(numeroPagina);
        setGrupoSeleccionadoId(null); 
    };

    const renderizarPaginacion = () => { 
        let items = [];
        for (let number = 1; number <= totalPaginas; number++) {
            items.push(
                <Pagination.Item 
                    key={number} 
                    active={number === paginaActual} 
                    onClick={() => paginar(number)}
                >
                    {number}
                </Pagination.Item>,
            );
        }
        
        return (
            <div className="d-flex justify-content-center mt-3">
                <Pagination>
                    <Pagination.Prev onClick={() => paginar(paginaActual - 1)} disabled={paginaActual === 1} />
                    {items}
                    <Pagination.Next onClick={() => paginar(paginaActual + 1)} disabled={paginaActual === totalPaginas} />
                </Pagination>
            </div>
        );
    };

    const filasTabla = gruposActuales.map(grupo => { 
        const grupoId = grupo.id; 
        const grupoNombre = grupo.nombre; 
        
        const radio = (
            <input 
                type="radio" 
                className="form-check-input"
                name="grupoSelection"
                checked={grupoSeleccionadoId === grupoId}
                onChange={() => handleCambioRadio(grupoId)}
            />
        );
        
        const botonModificar = (
            <BotonAgregar accion={() => iniciarModificacion(grupoId)}>
                <img src={imagenModificar} alt="icono modificar" style={{width: '15px'}} />
            </BotonAgregar>
        
        );
        
        const botonEliminar = (
            <BotonAgregar accion={() => handleEliminacion(grupoId, grupoNombre)}>
                <img src={imagenEliminar} alt="icono eliminar" style={{width: '15px'}} />
            </BotonAgregar>
            
        );

        const acciones = (
            <div style={{ display: 'flex', gap: '5px' }}>
                {botonModificar}
                {botonEliminar} 
            </div>
        );
        
        return [
            radio,
            grupo.sigla, 
            grupo.nombre, 
            grupo.unidad_academica, 
            grupo.director, 
            grupo.vicedirector, 
            grupo.correoElectronico,
            acciones
        ];
    });

    const renderizarContenidoModal = () => { 
        const tipo = infoModal.tipo;
        
        const areaTextoDetalleVisualizar = () => (
            <div>
                <p style={{ 
                    whiteSpace: 'pre-wrap', 
                    padding: '10px', 
                    border: '1px solid #ccc', 
                    minHeight: '100px',
                    backgroundColor: '#f8f9fa'
                }}>
                    {contenidoDetalle.contenido.trim() === "" 
                        ? `El campo "${infoModal.titulo}" para el grupo seleccionado está vacío.` 
                        : contenidoDetalle.contenido
                    }
                </p>
                <div style={{ textAlign: 'right', marginTop: '15px' }}>
                    <Button onClick={iniciarEdicionDetalle} variant="primary">
                        Modificar
                    </Button>
                </div>
            </div>
        );

        const areaTextoDetalleEditable = () => (
            <Form onSubmit={handleEnvioDetalle}>
                <FloatingLabel 
                    controlId="floatingTextareaDetalle" 
                    label="Contenido"
                >
                    <Form.Control
                        as="textarea"
                        placeholder="Escribe el contenido aquí..."
                        value={contenidoDetalle.contenido}
                        onChange={manejarCambioDetalle}
                        style={{ height: '200px' }}
                    />
                </FloatingLabel>
                <div style={{ textAlign: 'right', marginTop: '15px' }}>
                    <Button type="submit" variant="success">Guardar Cambios</Button>
                    <Button 
                        type="button" 
                        variant="secondary" 
                        onClick={() => setInfoModal(prev => ({ ...prev, tipo: 'verDetalle' }))}
                        style={{ marginLeft: '10px' }}
                    >
                        Cancelar
                    </Button>
                </div>
            </Form>
        );

        switch(tipo) {
            case 'agregar':
                return (
                    <Form onSubmit={handleEnvio} key={claveFormulario}> 
                        <FormularioGrupo 
                            data={datosNuevoGrupo} 
                            handleChange={handleFormularioNuevo}
                            isModifying={false}
                        />
                    </Form>
                );
            case 'modificar':
                return (
                    <Form onSubmit={handleActualizacion}>
                        <FormularioGrupo 
                            data={datosFormularioGrupo} 
                            handleChange={handleCambioFormularioExistente}
                            isModifying={true}
                        />
                    </Form>
                );
            
            case 'verDetalle':
                return areaTextoDetalleVisualizar();
            
            case 'modificarDetalle':
                return areaTextoDetalleEditable();

            default:
                return <p>Contenido no definido para este modal.</p>; 
        }
    };
    
    return (
        <div>
            <div>
                <div className="row container-fluid grupo">
                    <h1 className="col-2">Grupos:</h1>
                    <div className="col-8"></div>
                    <div className="col-2">
                        <BotonAgregar className="boton-agregar" accion={agregarGrupo}> 
                            <img className="imagenMas" src={imagenMas} alt="imagen mas"/>
                            Agregar Grupo
                        </BotonAgregar>
                    </div>
                </div>
                <div className="row container-fluid">
                    <div className="col-1"></div>
                    <div className="col-10">
                        <Tabla 
                            columnas={columnas}
                            filas={filasTabla} 
                        />
                        
                        {renderizarPaginacion()}
                        
                    </div>
                    <div className="col-1"></div>
                </div>
                
                <div className="row container-fluid mt-4">
                    <div className="col-12 d-flex justify-content-end gap-3">
                        <Boton texto={"Ver Planificacion"} accion={verPlanificacion}></Boton>
                        <Boton texto={"Ver Objetivos"} accion={verObjetivos}></Boton>
                        <Boton texto={"Ver Organigrama"} accion={verOrganigrama}></Boton>
                        <Boton texto={"Ver Consejo Ejecutivo"} accion={verConsejoEjecutivo}></Boton>
                    </div>
                </div>

                <ModalFormularios
                    show={mostrarModal}
                    onHide={() => setMostrarModal(false)}
                    titulo={infoModal.titulo}
                >
                    {renderizarContenidoModal()}
                </ModalFormularios>
            </div>
            <p>
                tamanio total {tamanio}
            </p>
        </div>
    )
}

export default Grupo;