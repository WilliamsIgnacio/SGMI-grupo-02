import React from "react";
import Container from 'react-bootstrap/Container';
import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import { NavDropdown } from "react-bootstrap";
import imagenUser from '../images/user-img.png';
import "./Navbar.css";
import iconoCerrarSesion from '../images/logoCerrarSesion.png';


function navbar() {

    return (
        <Navbar expand="lg" className="bg-body-tertiary">
            <Container fluid>
                <Navbar.Brand className="titulo" href="/grupo">SGMI</Navbar.Brand>
                <Navbar.Toggle aria-controls="navbarScroll" />
                <Navbar.Collapse id="navbarScroll">
                    <Nav
                        className="me-auto my-2 my-lg-0"
                        style={{ maxHeight: '100px' }}
                        navbarScroll
                    >
                        <Nav.Link className="link" href="/grupo/planificacion">Planificacion</Nav.Link>
                        <Nav.Link className="link" href="/grupo/planificacion/personal">Personal</Nav.Link>
                        <Nav.Link className="link" href="/grupo/planificacion/proyecto">Proyectos</Nav.Link>
                        <Nav.Link className="link" href="/grupo/planificacion/inventario">Equipamiento</Nav.Link>
                    </Nav>
                    <div className="d-flex align-items-center">
                        <div className="me-2">
                            Avril Lavigne
                        </div>
                        <NavDropdown title="" className="me-2" align="end">
                            <NavDropdown.Item href="/login">
                                <div className="d-flex-cerrar align-items-center">
                                    <span className="me-2">Cerrar Sesion</span>
                                    <img 
                                        className="iconoCerrarSesion" 
                                        src={iconoCerrarSesion} 
                                        alt="icono cerrar sesion" 
                                    />
                                </div>
                            </NavDropdown.Item>
                        </NavDropdown>
                        <figure className="figure">
                            <img className="imagen-user" src={imagenUser} alt="imagen del perfil del usuario" />
                        </figure>
                    </div>
                </Navbar.Collapse>
            </Container>
        </Navbar>
    );
} export default navbar