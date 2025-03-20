import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Box, CssBaseline, Toolbar } from '@mui/material';
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
import Login from './components/Login';

const rutasDisponibles = [
  { id: 1, path: '/productos', element: <Productos /> },
  { id: 2, path: '/ventas', element: <Ventas /> },
  { id: 3, path: '/administracion', element: <Administracion /> },
  { id: 4, path: '/panel', element: <Panel /> },
  { id: 5, path: '/abastecimiento', element: <Abastecimiento /> },
  { id: 6, path: '/cierre', element: <CierreCaja /> },
  { id: 7, path: '/configuracion', element: <Configuracion /> },
  { id: 8, path: '/config', element: <Config /> },
  { id: 9, path: '/movimientos', element: <MovimientosStock /> },
  { id: 10, path: '/inventario', element: <Inventario /> },
];

const handleLogin = (token, usuarioData) => {
  localStorage.setItem('auth_token', token);
  localStorage.setItem('usuario', JSON.stringify(usuarioData));
  window.location.href = "/";
};

function PrivateRoute({ element, permisoId, permisosUsuario }) {
  return permisosUsuario.includes(permisoId) ? element : <Navigate to="/" />;
}

function App() {
  const [usuario, setUsuario] = useState(null);
  const [permisosUsuario, setPermisosUsuario] = useState([]);

  useEffect(() => {
    const usuarioStorage = localStorage.getItem('usuario');
    let usuarioData = null;
    
    if (usuarioStorage && usuarioStorage !== "undefined") {
      try {
        usuarioData = JSON.parse(usuarioStorage);
      } catch (error) {
        console.error("Error al parsear usuarioStorage:", error);
      }
    }

    if (usuarioData && typeof usuarioData === 'object' && usuarioData.usuario) {
      setUsuario(usuarioData);
      const permisos = usuarioData.funciones ? usuarioData.funciones.map(f => f.id_funcion) : [];
      setPermisosUsuario(permisos);
    }
  }, []);

  return (
    <Router>
      <Box sx={{ display: 'flex' }}>
        <CssBaseline />
        {usuario && <BarraLateral permisosUsuario={permisosUsuario} />} 
        <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
          <Toolbar />
          <Routes>
            <Route path="/" element={usuario ? <h2>Bienvenido</h2> : <Login onLogin={handleLogin} />} />
            {rutasDisponibles.map(({ id, path, element }) => (
              <Route key={id} path={path} element={<PrivateRoute element={element} permisoId={id} permisosUsuario={permisosUsuario} />} />
            ))}
          </Routes>
        </Box>
      </Box>
    </Router>
  );
}

export default App;
