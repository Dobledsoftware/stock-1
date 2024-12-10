import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import BarraLateral from './components/BarraLateral';
import Stock from './pantallas/Stock';
import Ventas from './pantallas/Ventas';
import Administracion from './pantallas/Administracion';


import styled from 'styled-components';

// Estilo para el título de bienvenida
const Bienvenida = styled.h1`
  font-size: 2rem;
  color: #4CAF50;
  text-align: center;
  margin-top: 20px;
`;

// Estilo para la leyenda
const Leyenda = styled.p`
  font-size: 1rem;
  color: #555;
  text-align: center;
  margin-top: 10px;
  font-style: italic;
`;

function App() {
  return (
    <Router>
      <div style={{ display: "flex" }}>
        <BarraLateral />
        <main style={{ marginLeft: "240px", padding: "20px", width: "100%" }}>
          {/*<Bienvenida>Bienvenido a tu Panel de Administración</Bienvenida>
           Leyenda que da confianza al usuario 
          <Leyenda>
            Puedes usar el sistema de manera confiable y segura. Todos los datos están protegidos y son privados.
          </Leyenda>*/}
          <Routes>
            <Route path="/stock" element={<Stock />} />
            <Route path="/ventas" element={<Ventas />} />
            <Route path="/administracion" element={<Administracion />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
