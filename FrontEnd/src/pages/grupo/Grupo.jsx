import React, { useEffect } from "react";
import { useParams } from "react-router-dom"
import "./Grupo.css";


import CabeceraTabla from "../../components/CabeceraTabla";
import Tabla from "../../components/Tabla";
import Boton from "../../components/Boton";
import BotonAgregar from "../../components/BotonAgregar";
import imagenMas from "../../images/mas.png"
//import Paginacion from "../../components/Paginacion";

import { getGrupos } from "../../services/GrupoService";


function Grupo() {

    const columnas = ["Sigla", "Nombre", "Unidad Academica", "Director/a", "Vicedirector/a", "Correo Electronico"];
    const filasPrueba = [
        ["S.M.O.P", "Smooth Operator", "Ferrari", "Carlos Sainz JR.", "Charles Leclerc", "ferrari@gmail.com"],
        ["L.I.N.S.I", "Laboratorio de ingenieria en sistemas de informacion", "frlp", "Milagros Crespo", "Martina Garcia", "linsi@hotmail.com"]
    ];

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

    function agregarGrupo(){
        console.log("agregar grupo");
    }

    function verPlanificacion(){
        console.log("Ver Planificacion");
    }

    function verObjetivos(){
        console.log("Ver objetivos");
    }

    function verOrganigrama(){
        console.log("Ver Organigrama");
    }

    function verConsejoEjecutivo(){
        console.log("Ver Consejo Ejecutivo");
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
            </div>
        </div>
    )
}

export default Grupo