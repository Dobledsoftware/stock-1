import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import BarraLateral from './components/BarraLateral';
import Productos from './pantallas/Productos';
import Ventas from './pantallas/Ventas';
import Administracion from './pantallas/Administracion';
import Panel from './pantallas/Panel';
import Abastecimiento from './pantallas/Abastecimiento';
import CierreCaja from './pantallas/CierreCaja';
import Configuracion from './pantallas/Configuracion';
import Config from './pantallas/Config';
import MovimientosStock from './pantallas/Movimientos';
import Inventario from './pantallas/Inventario';
import 'font-awesome/css/font-awesome.min.css';
import styled from 'styled-components';

// Contenedor principal para la aplicación
const AppContainer = styled.div`
  display: flex;
  height: 100vh;
  overflow: hidden;
`;

// Contenido principal de la aplicación
const MainContent = styled.main`
  margin-left: ${(props) => (props.isSidebarOpen ? '240px' : '0')};
  flex-grow: 1;
  padding: 20px;
  background-color: #f4f4f9;
  overflow-y: auto;

  @media (max-width: 768px) {
    margin-left: ${(props) => (props.isSidebarOpen ? '10px' : '0')};
  }
`;

function App() {
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);

  return (
    <Router>
      <AppContainer>
        <BarraLateral isSidebarOpen={isSidebarOpen} setIsSidebarOpen={setIsSidebarOpen} />
        <MainContent isSidebarOpen={isSidebarOpen}>
          <Routes>
            <Route path="/productos" element={<Productos />} />
            <Route path="/panel" element={<Panel />} />
            <Route path="/ventas" element={<Ventas />} />
            <Route path="/cierre" element={<CierreCaja />} />
            <Route path="/configuracion" element={<Configuracion />} />
            <Route path="/config" element={<Config />} />
            <Route path="/movimientos" element={<MovimientosStock />} />
            <Route path="/inventario" element={<Inventario />} />
            
            <Route path="/abastecimiento" element={<Abastecimiento />} />
            <Route path="/administracion" element={<Administracion />} />
          </Routes>
        </MainContent>
      </AppContainer>
    </Router>
  );
}

export default App;
