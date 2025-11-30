import React from "react"
import { useParams } from "react-router-dom"
import Boton from "../../components/Boton"
import "./Planificacion.css"
import BotonAgregar from "../../components/BotonAgregar"
import imagenMas from "../../images/mas.png"
import ModalFormularios from "../../components/ModalFormularios";

function Planificacion() {

    const [modalShow, setModalShow] = React.useState(false);

    const [modalInfo, setModalInfo] = React.useState({
        titulo: '',
        contenido: null
    })

    function agregarPlanificacion() {
        setModalInfo({
            titulo: "Agregar Planificacion",
            contenido: (
                <div>
                    <p>AGREGAR PLANIFICACION</p>
                </div>
            )
        });
        setModalShow(true);
        
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

            <ModalFormularios
                    show={modalShow}
                    onHide={() => setModalShow(false)}
                    titulo={modalInfo.titulo}
                >
                    {modalInfo.contenido}
            </ModalFormularios>

        </div>
    )
}

export default Planificacion