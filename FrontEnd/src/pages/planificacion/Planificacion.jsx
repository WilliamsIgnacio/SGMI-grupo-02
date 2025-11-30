import { useParams } from "react-router-dom"
import Boton from "../../components/Boton"
import "./Planificacion.css"
import BotonAgregar from "../../components/BotonAgregar"
import imagenMas from "../../images/mas.png"
import { useState } from "react"
import { Button } from "bootstrap"

function Planificacion() {


    const [nuevaPlanificacion, setNuevaPlanificacion] = useState(0);
    const [anio, setAnio] = useState('');

    const planificaciones = [2021, 2022, 2023, 2024, 2025].reverse();
    const nombreGrupo = "S.M.O.P";

    function agregarPlanificacion() {
        if (nuevaPlanificacion == 0) {
            setNuevaPlanificacion(1);
        } else {
            setNuevaPlanificacion(0);
        }
    }

    function volverGrupo() {
        return alert("Volver")
    }

    function aceptarPlanificacion(){
        return alert(anio)
    }

    function controlAnio(event) {
        setAnio(event.target.value)
    }

    function accederPlanificacion(planificacion) {
        return alert(planificacion)
    }



    return (
        <div>
            <div className="row container-fluid">
                <div className="col">
                    <Boton texto={"Volver"} accion={volverGrupo}></Boton>
                </div>
                <div className="col">
                    <h1>Planificacion</h1>
                    <p>Grupo {nombreGrupo}</p>
                </div>
                <div className="col">
                    <BotonAgregar accion={agregarPlanificacion}>
                        <img className="imagenMas" src={imagenMas} alt="imagen mas"/>
                        Agregar Planificación
                    </BotonAgregar>
                    {nuevaPlanificacion == 1 &&
                        <div className="row">
                            <div className="col">
                                <input type="number" value={anio} onChange={controlAnio}/>
                            </div>
                            <div className="col">
                                <Boton texto={"aceptar"} accion={aceptarPlanificacion}></Boton>
                            </div>  
                        </div>
                    }
                </div>
            </div>
            <div className="row">
                {planificaciones.map((planificacion, index) => (
                    
                        <div className="col">
                            <Boton key={index} texto={planificacion} accion={() => accederPlanificacion(planificacion)}></Boton>
                        </div>
                    
                ))}
            </div>
        </div>
    )
}

export default Planificacion