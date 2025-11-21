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
        <div>
            <h1>bienvenido a SGMI</h1>
            <div className="row-container-fluid">
                <div className="col-3">
                    <Form>
                        <Form.Group className="mb-3" controlId="emailLogin">
                            <Form.Label>Correo Electrónico</Form.Label>
                            <Form.Control type="email" placeholder="tumail@ejemplo.com" />
                        </Form.Group>
                    
                        <Form.Group className="mb-3" controlId="contraseñaLogin">
                            <Form.Label>Contraseña</Form.Label>
                            <Form.Control type="password" placeholder="contraseña" />
                        </Form.Group>
                    </Form>
                </div>
            </div>

            <img className="imagen-logo" src={imagenLogin} alt="imagen login" width={"450px"} height={"300px"}/>
    
            <Boton texto={"Iniciar Sesión"} accion={iniciarSesion}></Boton>
        </div>
    )
}

export default Login