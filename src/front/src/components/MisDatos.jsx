// eslint-disable-next-line no-unused-vars
import React from 'react';
import '../styles/MisDatos.css'; // Asegúrate de tener este archivo de estilos

const MisDatos = () => {
    // Obtener datos del usuario del localStorage
    const nombre = localStorage.getItem('nombre');
    const apellido = localStorage.getItem('apellido');
    const cuil = localStorage.getItem('cuil'); // Asegúrate de que la clave sea correcta
    const legajo = localStorage.getItem('legajo'); // Asegúrate de que la clave sea correcta
    const email = localStorage.getItem('email'); // Asegúrate de que la clave sea correcta

    return (
        <div className="credencial-container">
            <div className="credencial">
                <div className="credencial-header">
                    <h2>Credencial de Usuario</h2>
                </div>
                <div className="credencial-body">
                    <p><strong>Nombre:</strong> {nombre}</p>
                    <p><strong>Apellido:</strong> {apellido}</p>
                    <p><strong>CUIL:</strong> {cuil}</p>
                    <p><strong>Legajo:</strong> {legajo}</p>
                    <p><strong>Email:</strong> {email}</p>
                </div>
            </div>
        </div>
    );
};

export default MisDatos;
