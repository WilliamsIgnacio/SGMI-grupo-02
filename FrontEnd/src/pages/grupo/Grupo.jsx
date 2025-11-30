import React, { useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom"
import "./Grupo.css";
import { useState } from "react";


import CabeceraTabla from "../../components/CabeceraTabla";
import Tabla from "../../components/Tabla";
import Boton from "../../components/Boton";
import BotonAgregar from "../../components/BotonAgregar";
import imagenMas from "../../images/mas.png";
import ModalFormularios from "../../components/ModalFormularios";
import FloatingLabel from 'react-bootstrap/FloatingLabel';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';

import { getGrupos } from "../../services/GrupoService";


function Grupo() {

    const [modalShow, setModalShow] = React.useState(false);

    const columnas = ["Sigla", "Nombre", "Unidad Academica", "Director/a", "Vicedirector/a", "Correo Electronico"];
    const filasPrueba = [
        ["S.M.O.P", "Smooth Operator", "Ferrari", "Carlos Sainz JR.", "Charles Leclerc", "ferrari@gmail.com"],
        ["L.I.N.S.I", "Laboratorio de ingenieria en sistemas de informacion", "frlp", "Milagros Crespo", "Martina Garcia", "linsi@hotmail.com"]
    ];

    const navigate = useNavigate();

    const [modalInfo, setModalInfo] = React.useState({
        titulo: '',
        contenido: null
    })

/*
    useEffect(() => {
        fetchGrupos();
    }, []);

    const fetchGrupos = async () => {

        try {
            const data = await getGrupos();
            setGrupos(data);
        } catch (error) {
            console.error("Error al obtener los grupos:", error);
        }
    };
*/

    function modificarObjetivos() {
        setModalInfo({
            titulo: "Modificar Grupo",
            contenido: (
                <div>
                    <FloatingLabel controlId="floatingTextarea2">
                        <Form.Control
                            as="textarea"
                            placeholder="Objetivos"
                            style={{ height: '200px' }}
                        />
                    </FloatingLabel> 
                    <button type="submit" className="boton-aceptar-form">Aceptar</button>
                </div>
            )
        });
        setModalShow(true);
    }

    function modificarConsejo() {
        setModalInfo({
            titulo: "Modificar Consejo",
            contenido: (
                <div>
                    <FloatingLabel controlId="floatingTextarea2">
                        <Form.Control
                            as="textarea"
                            placeholder="Objetivos"
                            style={{ height: '200px' }}
                        />
                    </FloatingLabel>
                    <button type="button">Aceptar</button>
                </div>
            )
        });
        setModalShow(true);
    }

    function modificarOrganigrama() {
        setModalInfo({
            titulo: "Modificar Organigrama",
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


    function agregarGrupo(){
        setModalInfo({
            titulo: "Agregar Grupo",
            contenido: (
                <div>
                    <Form>
                        <Row className="mb-3">
                            <Form.Group as={Col} controlId="formGridSigla">
                                <Form.Label>Sigla</Form.Label>
                                <Form.Control type="sigla" placeholder="Sigla del grupo" />
                            </Form.Group>

                            <Form.Group as={Col} controlId="formGridNombre">
                                <Form.Label>Nombre</Form.Label>
                                <Form.Control type="nombreGrupo" placeholder="Nombre del Grupo" />
                            </Form.Group>
                        </Row>

                        <Form.Group className="mb-3" controlId="formGridUnidadAcademica">
                            <Form.Label>Unidad Académica</Form.Label>
                            <Form.Control placeholder="p. ej: Facultad Regional La Plata" />
                        </Form.Group>

                        <Form.Group className="mb-3" controlId="formGridEmail">
                            <Form.Label>Correo Electrónico</Form.Label>
                            <Form.Control placeholder="correogrupo@gmail.com" />
                        </Form.Group>

                        <Row className="mb-3">
                            <Form.Group as={Col} controlId="formGridDirector">
                            <Form.Label>Director/a</Form.Label>
                            <Form.Control placeholder="Nombre y Apellido"/>
                            </Form.Group>

                            <Form.Group as={Col} controlId="formGridVicedirector">
                            <Form.Label>Vicedirector/a</Form.Label>
                            <Form.Control placeholder="Nombre y Apellido"/>
                            </Form.Group>
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

    function verPlanificacion(){
        navigate("planificacion");
    }

    function verObjetivos(){
        setModalInfo({
            titulo: "Objetivos del grupo",
            contenido: (
                <div>
                    <p>Aca irian los objetivos</p>
                    <Boton texto={"Modificar"} accion={modificarObjetivos}>
                    </Boton>
                </div>
            )
        });
        setModalShow(true);
    }

    function verOrganigrama(){
        setModalInfo({
            titulo: "Organigrama del Grupo",
            contenido: (
                <div>
                    <p>ORGANIGRAMA</p>
                    <Boton texto={"Modificar"} accion={modificarOrganigrama}></Boton>
                </div>
            )
        });
        setModalShow(true);
    }

    function verConsejoEjecutivo(){
        setModalInfo({
            titulo: "Consejo ejecutivo",
            contenido: (
                <div>
                    <p>Avril <br/> Nacho</p>
                    <Boton texto={"Modificar"} accion={modificarConsejo}>
                    </Boton>
                </div>
            )
        });
        setModalShow(true);
    }

    return (
        <div>
            <div>
                <div className="row container-fluid">
                    <h1 className="col-2">Grupos:</h1>
                    <div className="col-8"></div>
                    <div className="col-2">
                        <BotonAgregar accion={agregarGrupo}> 
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
                            filas={filasPrueba}
                        >
                        </Tabla>
                    </div>
                    <div className="col-1"></div>
                </div>
                <div className="row container-fluid">
                    <div className="col-3">
                        <Boton texto={"Ver Planificacion"} accion={verPlanificacion}></Boton>
                    </div>
                    <div className="col-3">
                        <Boton texto={"Ver Objetivos"} accion={verObjetivos}></Boton>
                    </div>
                    <div className="col-3">
                        <Boton texto={"Ver Organigrama"} accion={verOrganigrama}></Boton>
                    </div>
                    <div className="col-3">
                        <Boton texto={"Ver Consejo ejecutivo"} accion={verConsejoEjecutivo}></Boton>
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

export default Grupo