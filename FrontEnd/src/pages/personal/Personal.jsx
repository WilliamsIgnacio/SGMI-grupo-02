import React from "react";
import { useParams } from "react-router-dom"

import Tabla from "../../components/Tabla";
import CabeceraTabla from "../../components/CabeceraTabla";
import Boton from "../../components/Boton";
import BotonAgregar from "../../components/BotonAgregar";
import imagenMas from "../../images/mas.png"
import "./Personal.css"

function Personal() {

    const columnas = ["Codigo", "Nombre", "Apellido", "Horas Semanales", "Area"];
    const datosPrueba = [["001", "Carla", "Sanchez", "40", "Soporte"], ["002", "Carlos", "Sainz", "20", "Profesional"], ["003", "Carolina", "Suarez", "30", "Profesional"]];

    function agregarPersonal() {
        return alert("agregar personal");      
    }

    function verDescripcion() {
        return alert("ver descripcion");
    }
    
    function desvincular() {
        return alert("desvincular");
        
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
            </div>
        </div> 
    )
} 

export default Personal;