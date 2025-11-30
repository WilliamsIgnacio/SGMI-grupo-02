import React from "react";
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

function Proyecto() {

    const [modalShow, setModalShow] = React.useState(false);

    const columnas = ["Codigo", "Nombre", "Fecha de Inicio", "Fecha de Fin"];
    const datosPrueba = [["001", "Curso 1", "29-10-25", "31-12-25"], ["002", "Curso 2", "10-11-25", "31-03-26"]];

    const [modalInfo, setModalInfo] = React.useState({
        titulo: '',
        contenido: null
    })
    

    function agregarProyecto() {
        setModalInfo({
            titulo: "Agregar Proyecto",
            contenido: (
                <div>
                    <Form>
                        <Row className="mb-3">
                            <Form.Group as={Col} controlId="formGridNombre">
                                <Form.Label>Nombre</Form.Label>
                                <Form.Control placeholder="Nombre del Curso" />
                            </Form.Group>
                        </Row>

                        <Row className="mb-3">
                            <Form.Group as={Col} controlId="formGridFecha">
                                <Form.Label>Fecha de Inicio</Form.Label>
                                <Form.Control type="fecha" placeholder="p. ej: 10/11/2025" />
                            </Form.Group>

                            <Form.Group as={Col} controlId="formGridFecha">
                                <Form.Label>Fecha de Fin</Form.Label>
                                <Form.Control type="fecha" placeholder="p. ej: 10/12/2025" />
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
            titulo: "Descripcion",
            contenido: (
                <div>
                    <p>VER DESCRIPCION</p>
                </div>
            )
        });
        setModalShow(true);
    }

    function modificarLogros() {
        setModalInfo({
            titulo: "Modificar Logros",
            contenido: (
                <div>
                    <FloatingLabel controlId="floatingTextarea2">
                        <Form.Control
                            as="textarea"
                            style={{ height: '200px' }}
                        />
                    </FloatingLabel>
                    <button type="button">Aceptar</button>
                </div>
            )
        });
        setModalShow(true);
    }

    function verLogros() {
        setModalInfo({
            titulo: "Logros",
            contenido: (
                <div>
                    <p>aca van los logros</p>
                    <Boton texto={"Modificar"} accion={modificarLogros}></Boton>
                </div>
            )
        });
        setModalShow(true);
        
    }

    function modificarDificultades() {
        setModalInfo({
            titulo: "Modificar Dificultades",
            contenido: (
                <div>
                    <FloatingLabel controlId="floatingTextarea2">
                        <Form.Control
                            as="textarea"
                            style={{ height: '200px' }}
                        />
                    </FloatingLabel>
                    <button type="button">Aceptar</button>
                </div>
            )
        });
        setModalShow(true);
    }

    function verDificultades() {
        setModalInfo({
            titulo: "Dificultades",
            contenido: (
                <div>
                    <p>Aca se ven las Dificultades</p>
                    <Boton texto={"Modificar"} accion={modificarDificultades}></Boton>
                </div>
            )
        });
        setModalShow(true);
    }

    return (
        <div>
            <div>
                <h1>
                    Proyectos
                </h1>
                <p>
                    Grupo S.M.O.P
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
                            filas = {datosPrueba} 
                        >
                        </Tabla>
                    </div>
                    <div className="col-1"></div>
                </div>

                <div className="row container-fluid">
                    <div className="col-4">
                        <Boton texto={"Volver"}></Boton>
                    </div>
                    <div className="col-3">
                        <Boton texto={"Ver Descripcion"} accion={verDescripcion}></Boton>
                    </div>
                    <div className="col-3">
                        <Boton texto={"Ver Logros"} accion={verLogros}></Boton>
                    </div>
                    <div className="col-2">
                        <Boton texto={"Ver Dificultades"} accion={verDificultades}></Boton>
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

export default Proyecto