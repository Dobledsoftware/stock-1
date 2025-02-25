import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Box, CssBaseline, Toolbar } from '@mui/material';

// Importa el componente de la barra lateral refactorizada con Material UI
import BarraLateral from './components/BarraLateral';

// Importa tus pantallas o rutas
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

function App() {
  return (
    <Router>
      <Box sx={{ display: 'flex' }}>
        {/* CssBaseline normaliza estilos y BarraLateral contiene el Drawer */}
        <CssBaseline />
        <BarraLateral />
        {/* Área principal de contenido */}
        <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
          {/* Toolbar se utiliza para dejar un espacio que compense el AppBar o el encabezado del Drawer */}
          <Toolbar />
          <Routes>
            <Route path="/productos" element={<Productos />} />
            <Route path="/ventas" element={<Ventas />} />
            <Route path="/administracion" element={<Administracion />} />
            <Route path="/panel" element={<Panel />} />
            <Route path="/abastecimiento" element={<Abastecimiento />} />
            <Route path="/cierre" element={<CierreCaja />} />
            <Route path="/configuracion" element={<Configuracion />} />
            <Route path="/config" element={<Config />} />
            <Route path="/movimientos" element={<MovimientosStock />} />
            <Route path="/inventario" element={<Inventario />} />
          </Routes>
        </Box>
      </Box>
    </Router>
  );
}

export default App;
