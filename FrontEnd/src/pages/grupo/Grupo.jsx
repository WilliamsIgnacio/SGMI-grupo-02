import React, { useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom"
import "./Grupo.css";
import { useState } from "react";

import CabeceraTabla from "../../components/CabeceraTabla";
import Tabla from "../../components/Tabla";
import Boton from "../../components/Boton";
import BotonAgregar from "../../components/BotonAgregar";
import imagenMas from "../../images/mas.png";

import { getGrupos, getGrupo, createGrupo, updateGrupo, deleteGrupo } from "../../services/GrupoService";

//componentes bootstrap
import ModalFormularios from "../../components/ModalFormularios";
import FloatingLabel from 'react-bootstrap/FloatingLabel';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';



function Grupo() {

    const [modalShow, setModalShow] = React.useState(false);

    const [grupos, setGrupos] = React.useState([]);

    const columnas = ["Sigla", "Nombre", "Unidad Academica", "Director/a", "Vicedirector/a", "Correo Electronico", "Acciones"];
    const filasPrueba = [
        ["S.M.O.P", "Smooth Operator", "Ferrari", "Carlos Sainz JR.", "Charles Leclerc", "ferrari@gmail.com"],
        ["L.I.N.S.I", "Laboratorio de ingenieria en sistemas de informacion", "frlp", "Milagros Crespo", "Martina Garcia", "linsi@hotmail.com"] ];
    

    const [modalInfo, setModalInfo] = React.useState({
        titulo: '',
        contenido: null
    })

    //manejar los grupos

    useEffect(() => {
        fetchGrupos();
    }, []);

    useEffect(() => {
        fetchGrupos();
    }, []);

    const fetchGrupos = async () => {
        try {
            const data = await getGrupos();
            setGrupos(data);
            console.log(data);
        } catch (error) {
            console.error("Error al obtener los grupos:", error);
        }
    };

    const filasTabla = grupos.map(grupo => {

        const grupoId = grupo.id; 

        const botonModificar = (
            <Boton 
                texto={"Modificar"} 
                accion={() => iniciarModificacion(grupoId)}
            />
        );

        return [
            grupo.sigla, 
            grupo.nombre, 
            grupo.unidad_academica, 
            grupo.director, 
            grupo.vicedirector, 
            grupo.correo,
            botonModificar 
        ];
    });

    const [grupoFormularioData, setGrupoFormularioData] = useState({ 
        sigla: '',
        nombre: '',
        unidad_academica: '',
        director: '',
        vicedirector: '',
        correo: ''
    });

    const [grupoModificarId, setGrupoModificarId] = useState(null)

    const [nuevoGrupoData, setNuevoGrupoData] = useState({
        sigla: '',
        nombre: '',
        unidad_academica: '',
        director: '',
        vicedirector: '',
        correo: ''
    });

    const handleFormulario = (e) => {
        const { id, value } = e.target;
        setNuevoGrupoData(prevData => ({
            ...prevData,
            [id]: value
        }));
    } 

    const handleSubmit = async (e) => {
    e.preventDefault(); 

        try {
            console.log("Enviando datos del nuevo grupo:", nuevoGrupoData);

            await createGrupo(nuevoGrupoData);
            setNuevoGrupoData({
                sigla: '',
                nombre: '',
                unidad_academica: '',
                director: '',
                vicedirector: '',
                correo: ''
            });

            await fetchGrupos(); 
            setModalShow(false); 
            
        } catch (error) {
            console.error("Error al crear el grupo:", error);
            alert(`Error al crear el grupo: ${error.message}`);
        }
    };

    const handleUpdate = async (e) => {
        e.preventDefault();

        if (!grupoModificarId) {
            console.error("No hay ID de grupo para actualizar.");
            return;
        }

        try {
            console.log(`Actualizando grupo ID: ${grupoModificarId} con datos:`, grupoFormularioData);

            await updateGrupo(grupoModificarId, grupoFormularioData);

            await fetchGrupos(); 

            setGrupoEditandoId(null);
            setGrupoFormularioData({ 
                sigla: '', nombre: '', unidad_academica: '', 
                director: '', vicedirector: '', correo: ''
            });

            setModalShow(false); 

        } catch (error) {
            console.error("Error al modificar el grupo:", error);
            alert(`Error al modificar el grupo: ${error.message}`);
        }
    };
    
    const iniciarModificacion = async (id) => {
        try {
            const grupoAModificar = await getGrupo(id);
            
            setGrupoEditandoId(id); 
            
            setGrupoFormularioData({
                sigla: grupoAModificar.sigla || '',
                nombre: grupoAModificar.nombre || '',
                unidadAcademica: grupoAModificar.unidad_academica || '',
                director: grupoAModificar.director || '',
                vicedirector: grupoAModificar.vicedirector || '',
                correo: grupoAModificar.correo || '',
            });

            mostrarFormularioModificacion(grupoAModificar.nombre); 

        } catch (error) {
            console.error("Error al cargar datos para modificar:", error);
            alert(`No se pudo cargar el grupo para edición: ${error.message}`);
        }
    };

    const mostrarFormularioModificacion = (nombreGrupo) => {
        setModalInfo({
            titulo: `Modificar Grupo: ${nombreGrupo}`,
            contenido: (
                <Form onSubmit={handleUpdate}>
                    <FormularioGrupoContent 
                        data={grupoFormularioData} 
                        handleChange={handleFormChange}
                        isModifying={true}
                    />
                </Form>
            )
        });
        setModalShow(true);
    };

    const FormularioGrupoContent = ({ data, handleChange, isModifying }) => (
        <>
            <Row className="mb-3">
                <Form.Group as={Col} controlId="sigla"> 
                    <Form.Label>Sigla</Form.Label>
                    <Form.Control 
                        type="text" 
                        placeholder="Sigla del grupo" 
                        id="sigla"
                        value={data.sigla}
                        onChange={handleChange}
                        required
                    />
                </Form.Group>

                <Form.Group as={Col} controlId="nombre">
                    <Form.Label>Nombre</Form.Label>
                    <Form.Control 
                        type="text" 
                        placeholder="Nombre del Grupo" 
                        id="nombre"
                        value={data.nombre}
                        onChange={handleChange}
                        required
                    />
                </Form.Group>
            </Row>

            <Form.Group className="mb-3" controlId="unidadAcademica">
                <Form.Label>Unidad Académica</Form.Label>
                <Form.Control 
                    placeholder="p. ej: Facultad Regional La Plata" 
                    id="unidadAcademica"
                    value={data.unidad_academica}
                    onChange={handleChange}
                    required
                />
            </Form.Group>

            <Form.Group className="mb-3" controlId="correo">
                <Form.Label>Correo Electrónico</Form.Label>
                <Form.Control 
                    type="email" 
                    placeholder="correogrupo@gmail.com" 
                    id="correo"
                    value={data.correo}
                    onChange={handleChange}
                    required
                />
            </Form.Group>

            <Row className="mb-3">
                <Form.Group as={Col} controlId="director">
                <Form.Label>Director/a</Form.Label>
                <Form.Control 
                    placeholder="Nombre y Apellido"
                    id="director"
                    value={data.director}
                    onChange={handleChange}
                    required
                />
                </Form.Group>

                <Form.Group as={Col} controlId="vicedirector">
                <Form.Label>Vicedirector/a</Form.Label>
                <Form.Control 
                    placeholder="Nombre y Apellido"
                    id="vicedirector"
                    value={data.vicedirector}
                    onChange={handleChange}
                    required
                />
                </Form.Group>
            </Row>
            <div style={{ textAlign: 'right', marginTop: '15px' }}>
                <Button variant="primary" type="submit">
                    {isModifying ? "Guardar Cambios" : "Agregar Grupo"}
                </Button>
            </div>
        </>
    );

    //funcion botones + ventanas pop up

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

        setGrupoModificarId(null),
        setGrupoFormularioData({sigla: '', nombre: '', unidad_academica: '', director: '', vicedirector: '', correo: ''})

        setModalInfo({
            titulo: "Agregar Grupo",
            contenido: (
                <div>
                    <Form onSubmit={handleSubmit}>
                        <Row className="mb-3">
                            <Form.Group as={Col} controlId="sigla">
                                <Form.Label>Sigla</Form.Label>
                                <Form.Control 
                                    type="text" 
                                    placeholder="Sigla del grupo" 
                                    id="sigla"
                                    value={setNuevoGrupoData.sigla}
                                    onChange={handleFormulario}
                                />
                            </Form.Group>

                            <Form.Group as={Col} controlId="nombre">
                                <Form.Label>Nombre</Form.Label>
                                <Form.Control 
                                    type="text" 
                                    placeholder="Nombre del Grupo"
                                    id="nombre"
                                    value={setNuevoGrupoData.nombre}
                                    onChange={handleFormulario}
                                />
                            </Form.Group>
                        </Row>

                        <Form.Group className="mb-3" controlId="unidad_academica">
                            <Form.Label>Unidad Académica</Form.Label>
                            <Form.Control 
                                placeholder="p. ej: Facultad Regional La Plata" 
                                id="unidad_academica"
                                value={setNuevoGrupoData.unidad_academica}
                                onChange={handleFormulario}    
                            />
                        </Form.Group>

                        <Form.Group className="mb-3" controlId="correo">
                            <Form.Label>Correo Electrónico</Form.Label>
                            <Form.Control 
                                type="email"
                                placeholder="correogrupo@gmail.com"
                                id="correo"
                                value={setNuevoGrupoData.correo}
                                onChange={handleFormulario}
                            />
                        </Form.Group>

                        <Row className="mb-3">
                            <Form.Group as={Col} controlId="director">
                            <Form.Label>Director/a</Form.Label>
                            <Form.Control 
                                type="text" 
                                placeholder="Nombre y Apellido"
                                id="director"
                                value={setNuevoGrupoData.director}
                                onChange={handleFormulario}    
                            />
                            </Form.Group>

                            <Form.Group as={Col} controlId="vicedirector">
                            <Form.Label>Vicedirector/a</Form.Label>
                            <Form.Control
                                type="text" 
                                placeholder="Nombre y Apellido"
                                id="vicedirector"
                                value={setNuevoGrupoData.vicedirector}
                                onChange={handleFormulario}
                            />
                            </Form.Group>
                        </Row>
                        <div style={{textAlign: 'right', marginTop: '15px'}}>
                            <Button variant="primary" type="submit" style={{backgroundColor: '#7b7b7b', borderColor: '#7b7b7b'}}>
                                Agregar
                            </Button>
                        </div>
                    </Form>
                </div>
            )
        });
        setModalShow(true);
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

    function verPlanificacion(){
        navigate("planificacion");
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
                            filas={filasTabla}
                            //filas={filasPrueba}
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