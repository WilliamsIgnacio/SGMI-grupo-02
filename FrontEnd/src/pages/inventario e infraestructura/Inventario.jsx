import React, { useState, useMemo } from "react";
import Boton from "../../components/Boton";
import BotonAgregar from "../../components/BotonAgregar";
import Tabla from "../../components/Tabla";
import imagenMas from "../../images/mas.png"
import "./Inventario.css"
import { Navigate } from "react-router-dom";
import ModalFormularios from "../../components/ModalFormularios";
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';
import FloatingLabel from 'react-bootstrap/FloatingLabel';
import Pagination from 'react-bootstrap/Pagination';
import imagenEliminar from "../../images/eliminar.png"
import imagenModificar from "../../images/modificar.png"

function Inventario() {

    const [vistaTabla, setVistaTabla] = useState(0);
    const [mostrarModal, setMostrarModal] = useState(false);

    const [codigoFilaSeleccionada, setCodigoFilaSeleccionada] = useState(null);
    const [paginaActual, setPaginaActual] = useState(1);
    const elementosPorPagina = 5;

    const columnasEquipamientoBase = ["Codigo", "Denominacion", "Fecha de Incorporacion", "Monto"];
    const columnasEquipamiento = ["Selección", ...columnasEquipamientoBase, "Acciones"];

    const datosEquipamientoOriginales = [
        ["001", "Auto F1", "29-10-25", "1000000"], 
        ["002", "Auto F1", "10-11-25", "300000"],
        ["003", "Simulador", "01-01-26", "50000"],
        ["004", "Taller", "15-02-26", "250000"],
        ["005", "Computadora", "01-03-26", "1500"],
        ["006", "Servidor", "10-04-26", "5000"],
    ];

    const columnasBibliografiaBase = ["Titulo", "Editorial", "Fecha de Publicacion", "Autores"];
    const columnasBibliografia = ["Selección", ...columnasBibliografiaBase, "Acciones"];

    const datosBibliografiaOriginales = [
        ["Bibliografia: Ayrton Senna", "FIA", "29-10-25", "Vivianne Senna"],
        ["Manual de Carreras", "Motorsport Ed.", "10-11-25", "Michael B."],
        ["Historia F1", "Grand Prix Pub.", "01-01-26", "Jenna W."],
    ];

    const [informacionModal, setInformacionModal] = React.useState({
        titulo: '',
        contenido: null
    })

    const manejarSeleccionFila = (codigo) => {
        setCodigoFilaSeleccionada(prevCodigo => prevCodigo === codigo ? null : codigo);
    };

    const modificarElemento = (datosFila) => {
        const tipo = vistaTabla === 0 ? "Equipamiento" : "Bibliografía";
        console.log(`Modificar ${tipo}:`, datosFila);
        setInformacionModal({
            titulo: `Modificar ${tipo}`,
            contenido: (
                <div>
                    <p>Formulario para modificar el elemento: **{datosFila[1] || datosFila[0]}**</p>
                    <Button variant="primary" onClick={() => setMostrarModal(false)}>Cerrar</Button>
                </div>
            )
        });
        setMostrarModal(true);
    };

    const eliminarElemento = (datosFila) => {
        const tipo = vistaTabla === 0 ? "Equipamiento" : "Bibliografía";
        console.log(`Eliminar ${tipo}:`, datosFila);
        setInformacionModal({
            titulo: `Eliminar ${tipo}`,
            contenido: (
                <div>
                    <p>¿Estás seguro de que quieres eliminar el elemento **{datosFila[1] || datosFila[0]}**?</p>
                    <Button variant="danger" onClick={() => { setMostrarModal(false); }}>Eliminar</Button>
                    <Button variant="secondary" onClick={() => setMostrarModal(false)} className="ms-2">Cancelar</Button>
                </div>
            )
        });
        setMostrarModal(true);
    };

    const datosActuales = vistaTabla === 0 ? datosEquipamientoOriginales : datosBibliografiaOriginales;
    const totalPaginas = Math.ceil(datosActuales.length / elementosPorPagina);

    const datosPaginados = useMemo(() => {
        const indiceInicio = (paginaActual - 1) * elementosPorPagina;
        const indiceFin = indiceInicio + elementosPorPagina;
        return datosActuales.slice(indiceInicio, indiceFin);
    }, [datosActuales, paginaActual, elementosPorPagina]);

    const filasTablaFinal = datosPaginados.map(fila => {
        const codigo = fila[0];
        const estaSeleccionado = codigoFilaSeleccionada === codigo;

        const seleccion = (
            <Form.Check
                type="radio" 
                name="seleccionInventario" 
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

    function cambiarVista() {
        setVistaTabla(prevVista => prevVista === 0 ? 1 : 0);
        setPaginaActual(1);
        setCodigoFilaSeleccionada(null);
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

    function agregarEquipamiento(){
        setInformacionModal({
            titulo: "Agregar equipamiento",
            contenido: (
                <div>
                    <Form>
                        <Row className="mb-3">
                            <Form.Group as={Col} controlId="controlCodigoEq">
                                <Form.Label>Codigo</Form.Label>
                                <Form.Control type="text" placeholder="Codigo del Equipamiento" />
                            </Form.Group>

                            <Form.Group as={Col} controlId="controlDenominacionEq">
                                <Form.Label>Denominacion</Form.Label>
                                <Form.Control placeholder="Denominacion del Equipamiento" />
                            </Form.Group>
                        </Row>
                    
                        <Row className="mb-3">
                            <Form.Group as={Col} controlId="controlFechaEq">
                                <Form.Label>Fecha de Incorporación</Form.Label>
                                <Form.Control type="text" placeholder="p. ej: 10/11/2025" />
                            </Form.Group>

                            <Form.Group as={Col} controlId="controlMontoEq">
                                <Form.Label>Monto</Form.Label>
                                <Form.Control placeholder="p. ej: $3000000" />
                            </Form.Group>
                        </Row>
                    
                        <Row className="mb-3">
                            <Form.Label>Descripcion</Form.Label>
                            <FloatingLabel controlId="controlDescripcionEq" label="Descripción">
                                <Form.Control
                                    as="textarea"
                                    style={{ height: '100px' }}
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

    function agregarBibliografia(){
        setInformacionModal({
            titulo: "Agregar Bibliografia",
            contenido: (
                <div>
                    <Form>
                        <Row className="mb-3">
                            <Form.Group as={Col} controlId="controlTituloBib">
                                <Form.Label>Título</Form.Label>
                                <Form.Control type="text" placeholder="Titulo" />
                            </Form.Group>
                        </Row>
                    
                        <Row className="mb-3">
                            <Form.Group as={Col} controlId="controlEditorialBib">
                                <Form.Label>Editorial</Form.Label>
                                <Form.Control placeholder="Editorial" />
                            </Form.Group>

                            <Form.Group as={Col} controlId="controlFechaBib">
                                <Form.Label>Fecha de Publicación</Form.Label>
                                <Form.Control type="text" placeholder="p. ej: 10/11/2025" />
                            </Form.Group>
                        </Row>
                    
                        <Row className="mb-3">
                            <Form.Label>Autores</Form.Label>
                            <FloatingLabel controlId="controlAutoresBib" label="Autores">
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
        const elementoSeleccionado = datosActuales.find(fila => fila[0] === codigoFilaSeleccionada);
        const tipo = vistaTabla === 0 ? "Equipamiento" : "Bibliografía";
        const nombre = elementoSeleccionado ? (elementoSeleccionado[1] || elementoSeleccionado[0]) : "Ninguno";
        
        const descripcionContenido = codigoFilaSeleccionada 
            ? `Mostrando descripción de ${tipo} con identificador: ${nombre}` 
            : `Por favor, selecciona un elemento de ${tipo} para ver la descripción.`;

        setInformacionModal({
            titulo: "Ver descripción",
            contenido: (
                <div>
                    <p>**{descripcionContenido}**</p>
                    <Button variant="secondary" onClick={() => setMostrarModal(false)}>Cerrar</Button>
                </div>
            )
        });
        setMostrarModal(true);
    }

    function funcionVolver() {
        return alert("Volver a la vista anterior");
    }

    return (
        <div className="Inventario">
            <div>
                <h1 className="titulo-inventario">
                    Equipamiento e Infraestructura
                </h1>
                <p className="grupo-seleccionado-inventario">
                    Grupo 1
                </p>
            </div>
            <div>
                <div className="row container-fluid equipamiento mt-3 justify-content-between align-items-center">
                    <div className="col-auto">
                        <Boton texto={"Cambiar a " + (vistaTabla === 0 ? "Bibliografía" : "Equipamiento")} accion={cambiarVista}></Boton>
                    </div>
                    <div className="col-auto">
                        {vistaTabla === 0 && 
                            <BotonAgregar accion={agregarEquipamiento}>
                                <img className="imagenMas" src={imagenMas} alt="imagen mas"/>
                                Agregar Equipamiento
                            </BotonAgregar>
                        }
                        {vistaTabla === 1 &&
                            <BotonAgregar accion={agregarBibliografia}>
                                <img className="imagenMas" src={imagenMas} alt="imagen mas"/>
                                Agregar Bibliografía
                            </BotonAgregar>
                        }
                    </div>
                </div>

                

                <div className="row container-fluid mt-3">
                    <div className="col-2"></div>
                        <div className="col-8 align-items-center justify-content-center">
                            <Tabla
                                columnas={vistaTabla === 0 ? columnasEquipamiento : columnasBibliografia}
                                filas={filasTablaFinal}
                            >
                            </Tabla>
                            {renderizarPaginacion()}
                        </div>
                    <div className="col-2"></div>
                </div>


                <div className="row container-fluid mt-3 align-items-center justify-content-start">
                    <div className="col-auto me-3">
                        <Boton texto={"Volver"} accion={funcionVolver}></Boton>
                    </div>
                    <div className="col-auto">
                        <Boton texto={"Ver Descripción"} accion={verDescripcion}></Boton>
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

export default Inventario