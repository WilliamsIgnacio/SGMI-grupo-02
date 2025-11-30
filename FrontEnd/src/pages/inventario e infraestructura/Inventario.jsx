import React, { useState } from "react";
import Boton from "../../components/Boton";
import BotonAgregar from "../../components/BotonAgregar";
import Tabla from "../../components/Tabla";
import imagenMas from "../../images/mas.png"
import "./Inventario.css"
import { Navigate } from "react-router-dom";


function Inventario() {

    const [tabla, setTabla] = useState(0);

    const columnasEquipamiento = ["Codigo", "Denominacion", "Fecha de Incorporacion", "Monto"];
    const datosPruebaEquipamiento = [["001", "Auto F1", "29-10-25", "1000000"], ["002", "Auto F1", "10-11-25", "300000"]];

    const columnasBibliografia = ["Titulo", "Editorial", "Fecha de Publicacion", "Autores"];
    const datosPruebaBibliografia = [["Bibliografia: Ayrton Senna", "FIA", "29-10-25", "Vivianne Senna"]];

    function agregarEquipamiento(){
        return alert("agregar equipamiento")
    }

    function agregarBibliografia(){
        return alert("agregar bibliografia")
    }

    function verDescripcion() {
        return alert("ver descripcion")
        
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
            </div>
        </div>  
    )
}

export default Inventario