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
        <div className="container-fluid login">
            <div className="row container-fluid login">
                <div className="col-3 login-container">
                    <h1 className="titulo-login">SGMI</h1>
                    <p>Sistema de Gestión de Memorias de<br></br> Grupos y Centros de Investigación</p>
                    <h3>¡Bienvenido de vuelta!</h3>
            
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
                    <Image className="imagen-iniciar-sesion" src={imagenLogin} alt="Imagen del login"></Image>
                </div>
            </div>
            
        </div>
    )
}

export default Login