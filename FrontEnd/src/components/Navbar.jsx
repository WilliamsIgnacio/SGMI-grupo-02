import React from "react";
import Container from 'react-bootstrap/Container';
import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';

function navbar() {
    return (
        <div className="row container-fluid">
            <div className="col-12">
                <Navbar bg="dark" data-bs-theme="dark">
                    <Container>
                        <Navbar.Brand href="#home">SGMI</Navbar.Brand>
                        <Nav className="me-auto">
                            <Nav.Link href="#home">Home</Nav.Link>
                            <Nav.Link href="#personal">Personal</Nav.Link>
                            <Nav.Link href="#proyetos">Proyectos</Nav.Link>
                            <Nav.Link href="#equipamiento">Equipamiento</Nav.Link>
                        </Nav>
                    </Container>
                </Navbar>
            </div>
        </div>
    )
} export default navbar