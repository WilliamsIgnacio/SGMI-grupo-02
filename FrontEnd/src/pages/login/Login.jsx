import { useParams } from "react-router-dom"
import { Form, Row, Col } from 'react-bootstrap';
import "./Login.css";
import Boton from "../../components/Boton";
import imagenLogin from "../../images/imagen login.jpeg";

function Login() {

    function iniciarSesion() {
        console.log("iniciar sesion")
    }

    return (
        <div className="container-fluid">
            <h1>Bienvenido de vuelta!</h1>
            <h3>Sistema de Gestión de Memorias de Grupos y Centros de Investigación</h3>
            <div className="row container-fluid">
                <div className="col-3">
                    <Form>
                        <Form.Group className="mb-3" controlId="emailLogin">
                            <Form.Label>Email</Form.Label>
                            <Form.Control type="email" placeholder="tumail@ejemplo.com" />
                        </Form.Group>
                    
                        <Form.Group className="mb-3" controlId="contraseñaLogin">
                            <Form.Label>Contraseña</Form.Label>
                            <Form.Control type="password" placeholder="contraseña" />
                        </Form.Group>
                    </Form>
                </div>
                <div className="col-9">
                    <img className="imagen-logo" src={imagenLogin} alt="imagen login" width={"950px"} height={"600px"}/>
                </div>
            </div>
            <Boton texto={"Iniciar Sesión"} accion={iniciarSesion}></Boton>
        </div>
    )
}

export default Login