import React from "react";
import { useParams } from "react-router-dom"
import CabeceraTabla from "../../components/CabeceraTabla"
import Boton from "../../components/Boton";
import BotonAgregar from "../../components/BotonAgregar";
import Tabla from "../../components/Tabla";
import imagenMas from "../../images/mas.png"
import "./Proyecto.css";

function Proyecto() {

    const columnas = ["Codigo", "Nombre", "Fecha de Inicio", "Fecha de Fin"];
    const datosPrueba = [["001", "Curso 1", "29-10-25", "31-12-25"], ["002", "Curso 2", "10-11-25", "31-03-26"]];

    function agregarProyecto() {
        return alert("agregar proyecto");      
    }

    function verDescripcion() {
        return alert("ver descripcion");
    }
    
    function verLogros() {
        return alert("ver logros");
        
    }

    function verDificultades() {
        return alert("ver dificultades");
    }

    return (
        <div>
            <div>
                <h1>
                    proyectos
                </h1>
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
                    <div className="col-3">
                        <Boton texto={"Ver Descripcion"} accion={verDescripcion}></Boton>
                    </div>
                    <div className="col-3">
                        <Boton texto={"Ver Logros"} accion={verLogros}></Boton>
                    </div>
                    <div className="col-3">
                        <Boton texto={"Ver Dificultades"} accion={verDificultades}></Boton>
                    </div>
                </div>
                <div className="row container-fluid">
                    <div className="col-1">
                        <button>
                            Volver
                        </button>
                    </div>
                </div>
            </div>
        </div>    
    )
}

export default Proyecto