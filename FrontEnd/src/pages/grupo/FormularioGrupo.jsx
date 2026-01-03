import React from 'react';
import { Form, Button, Col, Row, FloatingLabel } from 'react-bootstrap';
import { useState } from 'react';


const FormularioGrupoContent = ({ data, handleChange, isModifying }) => {

    return (

        <>
            <Row className="mb-3">
                <Form.Group as={Col} controlId="sigla"> 
                    <Form.Label>Sigla</Form.Label>
                    <Form.Control 
                        type="text" 
                        placeholder="Sigla del grupo" 
                        value={data.sigla}
                        name="sigla" 
                        onChange={handleChange}
                        required
                    />
                </Form.Group>

                <Form.Group as={Col} controlId="nombre">
                    <Form.Label>Nombre</Form.Label>
                    <Form.Control 
                        type="text" 
                        placeholder="Nombre del Grupo" 
                        value={data.nombre}
                        name="nombre" 
                        onChange={handleChange}
                        required
                    />
                </Form.Group>
            </Row>

            <Form.Group className="mb-3" controlId="unidad_academica">
                <Form.Label>Unidad Académica</Form.Label>
                <Form.Control 
                    placeholder="p. ej: Facultad Regional La Plata" 
                    value={data.unidad_academica}
                    name="unidad_academica" 
                    onChange={handleChange}
                    required
                />
            </Form.Group>

            <Form.Group className="mb-3" controlId="correoElectronico">
                <Form.Label>Correo Electrónico</Form.Label>
                <Form.Control 
                    type="email" 
                    placeholder="correogrupo@gmail.com" 
                    value={data.correoElectronico}
                    name="correoElectronico" 
                    onChange={handleChange}
                    required
                />
            </Form.Group>

            <Row className="mb-3">
                <Form.Group as={Col} controlId="director">
                <Form.Label>Director/a</Form.Label>
                <Form.Control
                    type='text' 
                    placeholder="Nombre y Apellido"
                    value={data.director}
                    name="director" 
                    onChange={handleChange}
                    required
                />
                </Form.Group>

                <Form.Group as={Col} controlId="vicedirector">
                <Form.Label>Vicedirector/a</Form.Label>
                <Form.Control
                    type='text' 
                    placeholder="Nombre y Apellido"
                    value={data.vicedirector}
                    name="vicedirector" 
                    onChange={handleChange}
                    required
                />
                </Form.Group>
            </Row>

            <Row className="mb-3">
                <Form.Group className="mb-3" controlId="objetivos">
                <Form.Label>Objetivos</Form.Label>
                <Form.Control
                    as='textarea' 
                    placeholder="Objetivos del Grupo"
                    value={data.objetivos}
                    name="objetivos" 
                    required
                />
                </Form.Group>
            </Row>

            <Row className="mb-3">
                <Form.Group className="mb-3" controlId="organigrama">
                <Form.Label>Organigrama</Form.Label>
                <Form.Control
                    as='textarea' 
                    placeholder="Organigrama del Grupo"
                    value={data.organigrama}
                    name="Organigrama del grupo" 
                    required
                />
                </Form.Group>
            </Row>

            <Row className="mb-3">
                <Form.Group className="mb-3" controlId="consejoEjecutivo">
                <Form.Label>Consejo Ejecutivo</Form.Label>
                <Form.Control
                    as='textarea' 
                    placeholder="Consejo Ejecutivo del Grupo"
                    value={data.consejoEjecutivo}
                    name="consejoEjecutivo" 
                    required
                />
                </Form.Group>
            </Row>

            <div style={{ textAlign: 'right', marginTop: '15px' }}>
                <Button variant="primary" type="submit"> 
                    {isModifying ? "Guardar Cambios" : "Agregar Grupo"}
                </Button>
            </div>
        </>
    )    
};

export default FormularioGrupoContent;