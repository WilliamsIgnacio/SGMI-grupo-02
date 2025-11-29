import { useParams } from "react-router-dom"
import Boton from "../../components/Boton"
import "./Planificacion.css"
import BotonAgregar from "../../components/BotonAgregar"
import imagenMas from "../../images/mas.png"

function Planificacion() {

    function agregarPlanificacion() {
        return alert("agregar planificacion")
        
    }

    return (
        <div>
            <div>
                <h1>
                    planificacion
                </h1>
            </div>
            <div>
                <div className="row container-fluid">
                    <div className="col-10"></div>
                    <div className="col-2">
                        <BotonAgregar accion={agregarPlanificacion}>
                            <img className="imagenMas" src={imagenMas} alt="imagen mas"/>
                            Agregar Planificación
                        </BotonAgregar>
                    </div>
                </div>
            </div>

            <div> 
                {/*puse un boton normal aca pero hay que agregar toda la logica para traer los años y se muestren los botones por cada uno*/}
                <button>2025</button>
            </div>


        </div>
    )
}

export default Planificacion