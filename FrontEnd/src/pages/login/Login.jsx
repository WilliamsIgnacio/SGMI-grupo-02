import { useParams } from "react-router-dom"
import { Form, Row, Col } from 'react-bootstrap';
import "./Login.css";
import Boton from "../../components/Boton";
import imagenLogin from "../../images/imagen login.jpeg";
import Image from "react-bootstrap/Image";

function Login() {

    function iniciarSesion() {
        console.log("iniciar sesion")
    }

    return (
        <div className="container-fluid">
            <h1 className="titulo">SGMI</h1>
            <p>Sistema de Gestión de Memorias de<br></br> Grupos y Centros de Investigación</p>
            <h3>¡Bienvenido de vuelta!</h3>
            

            <div className="row container-fluid">
                <div className="col-3 login-container">
                    <Form>
                        <Form.Group className="mb-2" controlId="emailLogin">
                            <Form.Label>Email</Form.Label>
                            <Form.Control type="email" placeholder="tumail@ejemplo.com" />
                        </Form.Group>
                    
                        <Form.Group className="mb-2" controlId="contraseñaLogin">
                            <Form.Label>Contraseña</Form.Label>
                            <Form.Control type="password" placeholder="contraseña" />
                        </Form.Group>
                    </Form>
                    <Boton className="boton-iniciar-sesion" texto={"Iniciar Sesión"} accion={iniciarSesion}></Boton>
                </div>
                <div className="col imagen">
                    <Image src={imagenLogin} alt="Imagen del login"></Image>
                </div>
            </div>
            
        </div>
    )
}

export default Login