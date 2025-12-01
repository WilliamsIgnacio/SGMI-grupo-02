import React, { useState, useMemo } from "react";
import { useParams } from "react-router-dom"
import CabeceraTabla from "../../components/CabeceraTabla"
import Boton from "../../components/Boton";
import BotonAgregar from "../../components/BotonAgregar";
import Tabla from "../../components/Tabla";
import imagenMas from "../../images/mas.png"
import "./Proyecto.css";
import ModalFormularios from "../../components/ModalFormularios";
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';
import FloatingLabel from 'react-bootstrap/FloatingLabel';
import Pagination from 'react-bootstrap/Pagination';
import imagenEliminar from "../../images/eliminar.png"
import imagenModificar from "../../images/modificar.png"

function Proyecto() {

    const [mostrarModal, setMostrarModal] = useState(false);
    const [codigoFilaSeleccionada, setCodigoFilaSeleccionada] = useState(null);
    const [paginaActual, setPaginaActual] = useState(1);
    const elementosPorPagina = 5;

    const datosProyectoOriginales = [
        ["001", "Curso 1", "29-10-25", "31-12-25"],
        ["002", "Curso 2", "10-11-25", "31-03-26"],
        ["003", "Taller A", "01-01-26", "30-06-26"],
        ["004", "Seminario B", "15-02-26", "15-05-26"],
        ["005", "Implementación X", "01-03-26", "31-08-26"],
        ["006", "Capacitación Z", "10-04-26", "10-07-26"],
        ["007", "Desarrollo Alpha", "20-05-26", "20-10-26"],
        ["008", "Revisión Beta", "01-07-26", "30-09-26"],
    ];

    const columnas = ["Selección", "Código", "Nombre", "Fecha de Inicio", "Fecha de Fin", "Acciones"];

    const [informacionModal, setInformacionModal] = React.useState({
        titulo: '',
        contenido: null
    })

    const manejarSeleccionFila = (codigo) => {
        setCodigoFilaSeleccionada(prevCodigo => prevCodigo === codigo ? null : codigo);
    };

    const modificarProyecto = (datosFila) => {
        console.log("Modificar:", datosFila);
        setInformacionModal({
            titulo: `Modificar Proyecto: ${datosFila[1]}`,
            contenido: (
                <div>
                    <p>Formulario para modificar el proyecto: **{datosFila[1]}**</p>
                    <Button variant="primary" onClick={() => setMostrarModal(false)}>Cerrar</Button>
                </div>
            )
        });
        setMostrarModal(true);
    };

    const eliminarProyecto = (datosFila) => {
        console.log("Eliminar:", datosFila);
        setInformacionModal({
            titulo: "Eliminar Proyecto",
            contenido: (
                <div>
                    <p>¿Estás seguro de que quieres eliminar el proyecto **{datosFila[1]}**?</p>
                    <Button variant="danger" onClick={() => { setMostrarModal(false); }}>Eliminar</Button>
                    <Button variant="secondary" onClick={() => setMostrarModal(false)} className="ms-2">Cancelar</Button>
                </div>
            )
        });
        setMostrarModal(true);
    };

    const totalPaginas = Math.ceil(datosProyectoOriginales.length / elementosPorPagina);

    const datosPaginados = useMemo(() => {
        const indiceInicio = (paginaActual - 1) * elementosPorPagina;
        const indiceFin = indiceInicio + elementosPorPagina;
        return datosProyectoOriginales.slice(indiceInicio, indiceFin);
    }, [datosProyectoOriginales, paginaActual, elementosPorPagina]);

    const filasTablaFinal = datosPaginados.map(fila => {
        const codigo = fila[0];
        const estaSeleccionado = codigoFilaSeleccionada === codigo;

        const seleccion = (
            <Form.Check
                type="radio" 
                name="seleccionProyecto" 
                checked={estaSeleccionado}
                onChange={() => manejarSeleccionFila(codigo)}
            />
        );

        const botonModificar = (
            <BotonAgregar accion={() => iniciarModificacion(grupoId)}>
                <img src={imagenModificar} alt="icono modificar" style={{width: '15px'}} />
            </BotonAgregar>
        
        );
        
        const botonEliminar = (
            <BotonAgregar accion={() => manejarEliminacion(grupoId, grupoNombre)}>
                <img src={imagenEliminar} alt="icono eliminar" style={{width: '15px'}} />
            </BotonAgregar>
            
        );

        const acciones = (
            <div style={{ display: 'flex', gap: '5px' }}>
                {botonModificar}
                {botonEliminar} 
            </div>
        );

        return [seleccion, ...fila, acciones];
    });


    function agregarProyecto() {
        setInformacionModal({
            titulo: "Agregar Proyecto",
            contenido: (
                <div>
                    <Form>
                        <Row className="mb-3">
                            <Form.Group as={Col} controlId="controlNombre">
                                <Form.Label>Nombre</Form.Label>
                                <Form.Control placeholder="Nombre del Curso" />
                            </Form.Group>
                        </Row>

                        <Row className="mb-3">
                            <Form.Group as={Col} controlId="controlFechaInicio">
                                <Form.Label>Fecha de Inicio</Form.Label>
                                <Form.Control type="date" placeholder="p. ej: 10/11/2025" />
                            </Form.Group>

                            <Form.Group as={Col} controlId="controlFechaFin">
                                <Form.Label>Fecha de Fin</Form.Label>
                                <Form.Control type="date" placeholder="p. ej: 10/12/2025" />
                            </Form.Group>
                        </Row>

                        <Row className="mb-3">
                            <Form.Label>Descripcion</Form.Label>
                            <FloatingLabel controlId="controlDescripcion" label="Descripción del Proyecto">
                                <Form.Control
                                    as="textarea"
                                    style={{ height: '75px' }}
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
            titulo: "Descripción del Proyecto",
            contenido: (
                <div>
                    <p>**{descripcionContenido}**</p>
                    <Button variant="secondary" onClick={() => setMostrarModal(false)}>Cerrar</Button>
                </div>
            )
        });
        setMostrarModal(true);
    }

    function modificarLogros() {
        setInformacionModal({
            titulo: "Modificar Logros",
            contenido: (
                <div>
                    <FloatingLabel controlId="controlLogros">
                        <Form.Control
                            as="textarea"
                            style={{ height: '200px' }}
                        />
                    </FloatingLabel>
                    <button type="button" onClick={() => setMostrarModal(false)}>Aceptar</button>
                </div>
            )
        });
        setMostrarModal(true);
    }

    function verLogros() {
        setInformacionModal({
            titulo: "Logros",
            contenido: (
                <div>
                    <p>aca van los logros del proyecto seleccionado: {codigoFilaSeleccionada || 'N/A'}</p>
                    <Boton texto={"Modificar"} accion={modificarLogros}></Boton>
                </div>
            )
        });
        setMostrarModal(true);
        
    }

    function modificarDificultades() {
        setInformacionModal({
            titulo: "Modificar Dificultades",
            contenido: (
                <div>
                    <FloatingLabel controlId="controlDificultades">
                        <Form.Control
                            as="textarea"
                            style={{ height: '200px' }}
                        />
                    </FloatingLabel>
                    <button type="button" onClick={() => setMostrarModal(false)}>Aceptar</button>
                </div>
            )
        });
        setMostrarModal(true);
    }

    function verDificultades() {
        setInformacionModal({
            titulo: "Dificultades",
            contenido: (
                <div>
                    <p>Aca se ven las Dificultades del proyecto seleccionado: {codigoFilaSeleccionada || 'N/A'}</p>
                    <Boton texto={"Modificar"} accion={modificarDificultades}></Boton>
                </div>
            )
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
                    onClick={() => setPaginaActual(numero)}
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
        <div className="Proyecto">
            <div>
                <h1 className="titulo-proyecto">
                    Proyectos
                </h1>
                <p className="titulo-grupo-proyecto">
                    Grupo 1
                </p>
            </div>
            <div>
                <div className="row container-fluid">
                    <div className="col-10"></div>
                    <div className="col-2">
                        <BotonAgregar accion={agregarProyecto}>
                            <img className="imagenMas" src={imagenMas} alt="imagen mas"/>
                            Agregar Proyecto
                        </BotonAgregar>
                    </div>
                </div>
                <div className="row container-fluid">
                    <div className="col-2"></div>
                    <div className="col-8">
                        <Tabla
                            columnas={columnas}
                            filas = {filasTablaFinal} 
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

                    <div className="col-auto d-flex ms-auto gap-3"> 
                        <Boton texto={"Ver Descripcion"} accion={verDescripcion} />
                        <Boton texto={"Ver Logros"} accion={verLogros} />
                        <Boton texto={"Ver Dificultades"} accion={verDificultades} />
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

export default Proyecto