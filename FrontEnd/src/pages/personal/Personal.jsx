import React, { useState, useMemo } from "react";
import { useParams } from "react-router-dom"

import Tabla from "../../components/Tabla";
import CabeceraTabla from "../../components/CabeceraTabla";
import Boton from "../../components/Boton";
import BotonAgregar from "../../components/BotonAgregar";
import imagenMas from "../../images/mas.png"
import "./Personal.css"
import ModalFormularios from "../../components/ModalFormularios";
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';
import FloatingLabel from 'react-bootstrap/FloatingLabel';
import Pagination from 'react-bootstrap/Pagination';
import imagenEliminar from "../../images/eliminar.png"
import imagenModificar from "../../images/modificar.png"

function Personal() {


    const [mostrarModal, setMostrarModal] = useState(false); 
    const [codigoFilaSeleccionada, setCodigoFilaSeleccionada] = useState(null); 
    const [paginaActual, setPaginaActual] = useState(1); 
    const elementosPorPagina = 5;

    const datosPersonalOriginales = [ 
        ["001", "Carla", "Sanchez", "40", "Soporte"],
        ["002", "Carlos", "Sainz", "20", "Profesional"],
        ["003", "Carolina", "Suarez", "30", "Profesional"],
        ["004", "Juan", "Perez", "40", "Soporte"],
        ["005", "Maria", "Gomez", "35", "Profesional"],
        ["006", "Pedro", "Lopez", "20", "Soporte"],
        ["007", "Ana", "Martinez", "40", "Profesional"],
        ["008", "Luis", "Rodriguez", "30", "Soporte"],
        ["009", "Laura", "Fernandez", "35", "Profesional"],
        ["010", "Diego", "Garcia", "40", "Soporte"],
    ];

    
    const columnas = ["Selección", "Código", "Nombre", "Apellido", "Horas Semanales", "Área", "Acciones"]; 
    
    
    const manejarSeleccionFila = (codigo) => {
        setCodigoFilaSeleccionada(prevCodigo => prevCodigo === codigo ? null : codigo);
    };

    const modificarPersonal = (datosFila) => {
        console.log("Modificar:", datosFila);
        setInformacionModal({
            titulo: "Modificar Personal",
            contenido: (
                <div>
                    <p>Formulario para modificar a: **{datosFila[1]} {datosFila[2]}**</p>
                    <Button variant="primary" onClick={() => setMostrarModal(false)}>Cerrar</Button>
                </div>
            )
        });
        setMostrarModal(true);
    };

    const eliminarPersonal = (datosFila) => {
        console.log("Eliminar:", datosFila);
        setInformacionModal({
            titulo: "Eliminar Personal",
            contenido: (
                <div>
                    <p>¿Estás seguro de que quieres eliminar a **{datosFila[1]} {datosFila[2]}**?</p>
                    <Button variant="danger" onClick={() => { setMostrarModal(false); }}>Eliminar</Button>
                    <Button variant="secondary" onClick={() => setMostrarModal(false)} className="ms-2">Cancelar</Button>
                </div>
            )
        });
        setMostrarModal(true);
    };

    const totalPaginas = Math.ceil(datosPersonalOriginales.length / elementosPorPagina); 

    const datosPaginados = useMemo(() => {
        const indiceInicio = (paginaActual - 1) * elementosPorPagina; 
        const indiceFin = indiceInicio + elementosPorPagina; 
        return datosPersonalOriginales.slice(indiceInicio, indiceFin);
    }, [datosPersonalOriginales, paginaActual, elementosPorPagina]);

    const datosTablaFinal = datosPaginados.map(fila => {
        const codigo = fila[0];
        const estaSeleccionado = codigoFilaSeleccionada === codigo; 

        const seleccion = (
            <Form.Check
                type="radio" 
                name="seleccionPersonal" 
                checked={estaSeleccionado}
                onChange={() => manejarSeleccionFila(codigo)}
            />
        );

        const botonModificar = (
            <BotonAgregar accion={() => iniciarModificacion(grupoId)}>
                <img src={imagenModificar} alt="icono modificar" style={{width: '15px'}} />
            </BotonAgregar>
        
        );
        
        const acciones = (
            <div style={{ display: 'flex', gap: '3px', marginLeft:'20px'}}>
                {botonModificar}
            </div>
        );

        return [seleccion, ...fila, acciones];
    });


    const [informacionModal, setInformacionModal] = useState({ 
        titulo: '',
        contenido: null
    })

    function agregarPersonal() {
        setInformacionModal({
            titulo: "Agregar Personal",
            contenido: (
                <div className="Personal">
                    <Form>
                        <Row className="mb-3">
                            <Form.Group as={Col} controlId="controlTipoId"> 
                                <Form.Label>Seleccione tipo de identificacion</Form.Label>
                                <Form.Select aria-label="Documento de Identidad">
                                <option value="1">DNI</option>
                                <option value="2">Pasaporte</option>
                                </Form.Select>
                            </Form.Group>

                            <Form.Group as={Col} controlId="controlDocumento"> 
                                <Form.Label>Numero de Identificacion</Form.Label>
                                <Form.Control type="documento" placeholder="p. ej: 46786123" />
                            </Form.Group>
                        </Row>

                        <Row className="mb-3">
                            <Form.Group as={Col} controlId="controlNombre"> 
                                <Form.Label>Nombre</Form.Label>
                                <Form.Control placeholder="Nombre" />
                            </Form.Group>

                            <Form.Group as={Col} controlId="controlApellido">
                                <Form.Label>Apellido</Form.Label>
                                <Form.Control placeholder="Apellido" />
                            </Form.Group>
                        </Row>

                        <Row className="mb-3">
                            <Form.Group as={Col} controlId="controlHoras"> 
                            <Form.Label>Horas Semanales</Form.Label>
                            <Form.Control placeholder="p. ej: 45"/>
                            </Form.Group>

                            <Form.Group as={Col} controlId="controlPerfil">
                                <Form.Label>Perfil</Form.Label>
                                <Form.Select aria-label="Seleccion de Perfil">
                                <option value="1">Seleccione un perfil</option>
                                </Form.Select>
                            </Form.Group>
                        </Row>

                        <Row className="mb-3">
                            <Form.Label>Descripcion</Form.Label>
                            <FloatingLabel controlId="controlDescripcion" label="Descripción del Personal"> 
                                <Form.Control
                                    as="textarea"
                                    style={{ height: '75px' }}
                                />
                            </FloatingLabel> 
                        </Row>

                        <Row className="mb-3">
                            <Form.Label>Especialidad</Form.Label>
                            <FloatingLabel controlId="controlEspecialidad" label="Especialidad"> 
                                <Form.Control
                                    as="textarea"
                                    style={{ height: '45px' }}
                                />
                            </FloatingLabel> 
                        </Row>

                        <Button variant="primary" type="submit">
                            Agregar
                        </Button>
                    </Form>
                </div>
            )
        });
        setMostrarModal(true);     
    }

    function verDescripcion() {
        const descripcionContenido = codigoFilaSeleccionada 
            ? `Mostrando descripción para el código: ${codigoFilaSeleccionada}` 
            : 'Por favor, selecciona una fila para ver la descripción.';

        setInformacionModal({
            titulo: "Descripción de Personal",
            contenido: (
                <div>
                    <p>**{descripcionContenido}**</p>
                    <Button variant="secondary" onClick={() => setMostrarModal(false)}>Cerrar</Button>
                </div>
            )
        });
        setMostrarModal(true);
    }

    function desvincularPersonal() {
        setInformacionModal({
            titulo: "Desvincular",
            contenido: (
                <div>
                    <Form>
                        <Row className="mb-3">
                            <Form.Group as={Col} controlId="controlFechaDesvinculacion"> 
                                <Form.Label>Fecha de Desvinculación</Form.Label>
                                <Form.Control type="date" placeholder="p. ej: 10/11/2025" />
                            </Form.Group>
                        </Row>
                        <Button variant="danger" type="submit" className="me-2">
                            Confirmar Desvinculación
                        </Button>
                        <Button variant="secondary" onClick={() => setMostrarModal(false)}>
                            Cancelar
                        </Button>
                    </Form>
                </div>
            )
        })
    }
    
    function desvincular() {
        const desvincularContenido = codigoFilaSeleccionada 
            ? (
                <div>
                    <p>¿Deseas desvincular al personal con código: **{codigoFilaSeleccionada}**?</p>
                    <Boton texto={"Desvincular"} accion={desvincularPersonal}></Boton>
                </div>
            )
            : (
                <div>
                    <p>Por favor, selecciona una persona para desvincular.</p>
                    <Button variant="secondary" onClick={() => setMostrarModal(false)}>Cerrar</Button>
                </div>
            );

        setInformacionModal({
            titulo: "Desvincular",
            contenido: desvincularContenido
        });
        setMostrarModal(true);
    }

    const renderizarPaginacion = () => { 
        let items = [];
        for (let numero = 1; numero <= totalPaginas; numero++) { 
            items.push(
                <Pagination.Item 
                    key={numero} 
                    active={numero === paginaActual} 
                    onClick={() => setPaginaActual(numero)} // 
                >
                    {numero}
                </Pagination.Item>,
            );
        }

        return (
            <Pagination className="justify-content-center mt-3">
                <Pagination.Prev onClick={() => setPaginaActual(paginaActual - 1)} disabled={paginaActual === 1} />
                {items}
                <Pagination.Next onClick={() => setPaginaActual(paginaActual + 1)} disabled={paginaActual === totalPaginas} />
            </Pagination>
        );
    }

    return (

        <div>
            <div>
                <h1 className="personal-titulo">
                    Personal
                </h1>
                <p className="nombre-grupo-seleccionado">
                    Grupo 1
                </p>
            </div>
            {/* --- */}
            <div>
                <div className="row container-fluid">
                    <div className="col-10"></div>
                    <div className="col-2">
                        <BotonAgregar accion={agregarPersonal}>
                            <img className="imagenMas" src={imagenMas} alt="imagen mas"/>
                            Agregar Personal
                        </BotonAgregar>
                    </div>
                </div>
                <div className="row container-fluid">
                    <div className="col-2"></div>
                    <div className="col-8">
                        <Tabla
                            columnas={columnas}
                            filas = {datosTablaFinal} 
                        >
                        </Tabla>
                        {renderizarPaginacion()} 
                    </div>
                    <div className="col-1"></div>
                </div>

                <div className="row container-fluid mt-3 align-items-center justify-content-between">
                    <div className="col-auto"> 
                        <Boton texto={"Volver"}></Boton>
                    </div>
                    <div className="col-auto d-flex ms-auto"> 
                        <Boton 
                            texto={"Desvincular"} 
                            accion={desvincular} 
                            className="me-3"
                        />
                        <Boton 
                            texto={"Ver Descripción"} 
                            accion={verDescripcion}
                            className="ms-3"                         
                        />
                    </div>
                </div>

                <ModalFormularios
                    show={mostrarModal}
                    onHide={() => setMostrarModal(false)}
                    titulo={informacionModal.titulo}
                >
                    {informacionModal.contenido}
                </ModalFormularios>
            </div>
        </div> 
    )
} 

export default Personal;