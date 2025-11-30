import React from "react";
import { useParams } from "react-router-dom"
import CabeceraTabla from "../../components/CabeceraTabla"
import Boton from "../../components/Boton";
import BotonAgregar from "../../components/BotonAgregar";
import Tabla from "../../components/Tabla";
import imagenMas from "../../images/mas.png"
import "./Proyecto.css";
import ModalFormularios from "../../components/ModalFormularios";

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
                    <p>AGREGAR PROYECTO</p>
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
    
    function verLogros() {
        setModalInfo({
            titulo: "Logros",
            contenido: (
                <div>
                    <p>VER LOGROS</p>
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
                    <p>VER DIFICULTADES</p>
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