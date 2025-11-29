import React from "react";
import { useParams } from "react-router-dom";
import CabeceraTabla from "../../components/CabeceraTabla"
import Boton from "../../components/Boton";
import BotonAgregar from "../../components/BotonAgregar";
import Tabla from "../../components/Tabla";
import imagenMas from "../../images/mas.png"
import "./Inventario.css"


function Inventario() {

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

    return (
        <div>
            <div>
                <h1>
                    equipamiento e infraestructura
                </h1>
            </div>
            <div>
                <div className="row container-fluid">
                    <div className="col-10"></div>
                    <div className="col-2">
                        <BotonAgregar  accion={agregarEquipamiento}>
                            <img className="imagenMas" src={imagenMas} alt="imagen mas"/>
                            Agregar Equipamiento
                        </BotonAgregar>
                    </div>
                    <div className="col-2">
                        <BotonAgregar accion={agregarBibliografia}>
                            <img className="imagenMas" src={imagenMas} alt="imagen mas"/>
                            Agregar Bibliografia
                        </BotonAgregar>
                    </div>
                </div>
                <div className="row container-fluid">
                    <div className="col-2"></div>
                    <div className="col-8">
                        <Tabla
                            columnas={columnasEquipamiento}
                            filas = {datosPruebaEquipamiento} 
                        >
                        </Tabla>
                    </div>
                    <div className="col-1"></div>
                </div>

                <div className="row container-fluid">
                    <div className="col-2"></div>
                    <div className="col-8">
                        <Tabla
                            columnas={columnasBibliografia}
                            filas = {datosPruebaBibliografia} 
                        >
                        </Tabla>
                    </div>
                    <div className="col-1"></div>
                </div>

                <div className="row container-fluid">
                    <div className="col-3">
                        <Boton texto={"Ver Descripcion"} accion={verDescripcion}></Boton>
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

export default Inventario