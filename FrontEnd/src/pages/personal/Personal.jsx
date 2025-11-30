import React from "react";
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

function Personal() {

    const [modalShow, setModalShow] = React.useState(false);

    const columnas = ["Codigo", "Nombre", "Apellido", "Horas Semanales", "Area"];
    const datosPrueba = [["001", "Carla", "Sanchez", "40", "Soporte"], ["002", "Carlos", "Sainz", "20", "Profesional"], ["003", "Carolina", "Suarez", "30", "Profesional"]];

    const [modalInfo, setModalInfo] = React.useState({
        titulo: '',
        contenido: null
    })

    function agregarPersonal() {
        setModalInfo({
            titulo: "Agregar Personal",
            contenido: (
                <div>
                    <Form>
                        <Row className="mb-3">
                            <Form.Group as={Col} controlId="formGridNombre">
                                <Form.Label>Seleccione tipo de identificacion</Form.Label>
                                <Form.Select aria-label="Documento de Identidad">
                                <option value="1">DNI</option>
                                <option value="2">Pasaporte</option>
                                </Form.Select>
                            </Form.Group>

                            <Form.Group as={Col} controlId="formGridDocumento">
                                <Form.Label>Numero de Identificacion</Form.Label>
                                <Form.Control type="documento" placeholder="p. ej: 46786123" />
                            </Form.Group>
                        </Row>

                        <Row className="mb-3">
                            <Form.Group as={Col} controlId="formGridNombre">
                                <Form.Label>Nombre</Form.Label>
                                <Form.Control placeholder="Nombre" />
                            </Form.Group>

                            <Form.Group as={Col} controlId="formGridApellido">
                                <Form.Label>Apellido</Form.Label>
                                <Form.Control placeholder="Apellido" />
                            </Form.Group>
                        </Row>

                        <Row className="mb-3">
                            <Form.Group as={Col} controlId="formGridHoras">
                            <Form.Label>Horas Semanales</Form.Label>
                            <Form.Control placeholder="p. ej: 45"/>
                            </Form.Group>

                            <Form.Group as={Col} controlId="formGridNombre">
                                <Form.Label>Perfil</Form.Label>
                                <Form.Select aria-label="Documento de Identidad">
                                <option value="1">Seleccione un perfil</option>
                                </Form.Select>
                            </Form.Group>
                        </Row>

                        <Row className="mb-3">
                            <Form.Label>Descripcion</Form.Label>
                            <FloatingLabel controlId="floatingTextarea2">
                                <Form.Control
                                    as="textarea"
                                    style={{ height: '75px' }}
                                />
                            </FloatingLabel> 
                        </Row>

                        <Row className="mb-3">
                            <Form.Label>Especialidad</Form.Label>
                            <FloatingLabel controlId="floatingTextarea2">
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
        setModalShow(true);      
    }

    function verDescripcion() {
        setModalInfo({
            titulo: "dESCRIPCIoN",
            contenido: (
                <div>
                    <p>VER DESCRIPCION</p>
                </div>
            )
        });
        setModalShow(true);
    }

    function desvincularPersonal() {
        setModalInfo({
            titulo: "Desvincular",
            contenido: (
                <div>
                    <Form>
                        <Row className="mb-3">
                            <Form.Group as={Col} controlId="formGridDocumento">
                                <Form.Label>Fecha de Desvinculación</Form.Label>
                                <Form.Control type="documento" placeholder="p. ej: 10/11/2025" />
                            </Form.Group>
                        </Row>
                        <Button variant="primary" type="submit">
                            Agregar
                        </Button>
                        <Button variant="primary" type="submit">
                            Cancelar
                        </Button>
                    </Form>
                </div>
            )
        })
    }
    
    function desvincular() {
        setModalInfo({
            titulo: "Desvincular",
            contenido: (
                <div>
                    Aca irian los datos de la persona que se quiere desvincular
                    <Boton texto={"desvincular"} accion={desvincularPersonal}></Boton>
                </div>
            )
        });
        setModalShow(true);
        
    }

    return (

        <div>
            <div>
                <h1>
                    Personal
                </h1>
                <p>
                    Grupo S.M.O.P
                </p>
            </div>
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
                            filas = {datosPrueba} 
                        >
                        </Tabla>
                    </div>
                    <div className="col-1"></div>
                </div>

                <div className="row container-fluid">
                    <div className="col">
                        <Boton texto={"Volver"}></Boton>
                    </div>
                    <div className="col">
                        <Boton texto={"Ver Descripcion"} accion={verDescripcion}></Boton>
                    </div>
                    <div className="col">
                        <Boton texto={"Desvincular"} accion={desvincular}></Boton>
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

export default Personal;