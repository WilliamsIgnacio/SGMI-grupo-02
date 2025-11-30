import React, { useState } from "react";
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


function Inventario() {

    const [tabla, setTabla] = useState(0);

    const [modalShow, setModalShow] = React.useState(false);

    const columnasEquipamiento = ["Codigo", "Denominacion", "Fecha de Incorporacion", "Monto"];
    const datosPruebaEquipamiento = [["001", "Auto F1", "29-10-25", "1000000"], ["002", "Auto F1", "10-11-25", "300000"]];

    const columnasBibliografia = ["Titulo", "Editorial", "Fecha de Publicacion", "Autores"];
    const datosPruebaBibliografia = [["Bibliografia: Ayrton Senna", "FIA", "29-10-25", "Vivianne Senna"]];

    const [modalInfo, setModalInfo] = React.useState({
        titulo: '',
        contenido: null
    })

    function agregarEquipamiento(){
        setModalInfo({
            titulo: "Agregar equipamiento",
            contenido: (
                <div>
                    <Form>
                        <Row className="mb-3">
                            <Form.Group as={Col} controlId="formGridCodigo">
                                <Form.Label>Codigo</Form.Label>
                                <Form.Control type="codigo" placeholder="Codigo del Equipamiento" />
                            </Form.Group>

                            <Form.Group as={Col} controlId="formGridDenominacion">
                                <Form.Label>Denominacion</Form.Label>
                                <Form.Control placeholder="Denominacion del Equipamiento" />
                            </Form.Group>
                        </Row>
                    
                        <Row className="mb-3">
                            <Form.Group as={Col} controlId="formGridFecha">
                                <Form.Label>Fecha de Incorporación</Form.Label>
                                <Form.Control type="fecha" placeholder="p. ej: 10/11/2025" />
                            </Form.Group>

                            <Form.Group as={Col} controlId="formGridMonto">
                                <Form.Label>Monto</Form.Label>
                                <Form.Control placeholder="p. ej: $3000000" />
                            </Form.Group>
                        </Row>
                    
                        <Row className="mb-3">
                            <Form.Label>Descripcion</Form.Label>
                            <FloatingLabel controlId="floatingTextarea2">
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
        setModalShow(true);
    }

    function agregarBibliografia(){
        setModalInfo({
            titulo: "Agregar Bibliografia",
            contenido: (
                <div>
                    <Form>
                        <Row className="mb-3">
                            <Form.Group as={Col} controlId="formGridTitulo">
                                <Form.Label>Título</Form.Label>
                                <Form.Control type="titulo" placeholder="Titulo" />
                            </Form.Group>
                        </Row>
                        
                        <Row className="mb-3">
                            <Form.Group as={Col} controlId="formGridEditorial">
                                <Form.Label>Editorial</Form.Label>
                                <Form.Control placeholder="Editorial" />
                            </Form.Group>

                            <Form.Group as={Col} controlId="formGridFecha">
                                <Form.Label>Fecha de Incorporación</Form.Label>
                                <Form.Control type="fecha" placeholder="p. ej: 10/11/2025" />
                            </Form.Group>
                        </Row>
                    
                        <Row className="mb-3">
                            <Form.Label>Autores</Form.Label>
                            <FloatingLabel controlId="floatingTextarea2">
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
        setModalShow(true);
    }

    function verDescripcion() {
        setModalInfo({
            titulo: "Ver descripcion",
            contenido: (
                <div>
                    <p>Aca iria la descripcion</p>
                </div>
            )
        });
        setModalShow(true);
        
    }

    function funcionVolver() {
        return alert("volver")
    }

    function cambiarVista() {
        if (tabla == 0) {
            setTabla(1);
        } else {
            setTabla(0);
        }
    }

    return (
        <div>
            <div>
                <h1>
                    Equipamiento e Infraestructura
                </h1>
                <p>
                    Grupo S.M.O.P
                </p>
            </div>
            <div>
                <div className="row container-fluid">
                    <div className="col">
                        <Boton texto={"equipamiento infrastructura"} accion={cambiarVista}></Boton>
                    </div>
                    <div className="col">
                        {tabla == 0 && 
                            <BotonAgregar  accion={agregarEquipamiento}>
                                <img className="imagenMas" src={imagenMas} alt="imagen mas"/>
                                Agregar Equipamiento
                            </BotonAgregar>
                        }
                        {tabla == 1 &&
                            <BotonAgregar accion={agregarBibliografia}>
                                <img className="imagenMas" src={imagenMas} alt="imagen mas"/>
                                Agregar Bibliografia
                            </BotonAgregar>
                        }
                    </div>
                </div>

                
                <div className="row container-fluid">
                    <div className="col-2"></div>
                    <div className="col-8">
                        {tabla == 0 && 
                            <Tabla
                                columnas={columnasEquipamiento}
                                filas = {datosPruebaEquipamiento} 
                            >
                            </Tabla>
                        }
                        {tabla == 1 &&
                            <Tabla
                                columnas={columnasBibliografia}
                                filas = {datosPruebaBibliografia} 
                            >
                            </Tabla>
                        }
                    </div>
                    <div className="col-1"></div>
                </div>

                <div className="row container-fluid">
                    <div className="col">
                        <Boton texto={"Volver"} accion={funcionVolver}></Boton>
                    </div>
                    <div className="col">
                        <Boton texto={"Ver Descripcion"} accion={verDescripcion}></Boton>
                    </div>
                </div>

                <ModalFormularios
                    show={modalShow}
                    onHide={() => setModalShow(false)}
                    titulo={modalInfo.titulo}
                >
                    {modalInfo.contenido}
                </ModalFormularios>
            </div>
        </div>  
    )
}

export default Inventario