import { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import Login from './components/Login';
import Navbar from './components/Navbar';
import Recibos from './components/Recibos';
import Usuarios from './components/Usuarios';
import MisDatos from './components/MisDatos';
import ActivadorRecibos from './components/ActivadorRecibos';

const App = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  const handleLdapLogin = async (samaccountname, password) => {
    try {
      const response = await fetch('http://10.5.0.124:8000/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ samaccountname, password })
      });

      if (response.ok) {
        // Aquí puedes manejar tokens o información adicional
        setIsAuthenticated(true);
      } else {
        // Maneja errores de autenticación
        alert('Credenciales LDAP inválidas');
      }
    } catch (error) {
      console.error('Error en la autenticación LDAP:', error);
      alert('Error en la autenticación LDAP');
    }
  };

  const handleApiLogin = async (cuil, password) => {
    try {
      const response = await fetch('http://10.5.0.124:8000/api/login', { // Asegúrate de que esta URL sea correcta
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ cuil, password })
      });

      if (response.ok) {
        // Aquí puedes manejar tokens o información adicional
        setIsAuthenticated(true);
      } else {
        // Maneja errores de autenticación
        alert('Credenciales API inválidas');
      }
    } catch (error) {
      console.error('Error en la autenticación API:', error);
      alert('Error en la autenticación API');
    }
  };

  const handleLogout = () => {
    // Lógica para cerrar sesión, como eliminar tokens
    setIsAuthenticated(false);
    console.log('Cerrar sesión');
  };

  return (
    <Router>
      {!isAuthenticated ? (
        // Mostrar el login a pantalla completa si no está autenticado
        <Routes>
          <Route 
            path="/" 
            element={
              <Login 
                onLdapLogin={handleLdapLogin} 
                onApiLogin={handleApiLogin} 
              />
            } 
          />
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      ) : (
        // Mostrar la barra de navegación y rutas si está autenticado
        <>
          <Navbar onLogout={handleLogout} />
          <Routes>
            <Route path="/" element={<Navigate to="/recibos" />} />
            <Route path="/recibos" element={<Recibos />} />
            <Route path="/usuarios" element={<Usuarios />} />
            <Route path="/mis-datos" element={<MisDatos />} />
            <Route path="/activador-recibos" element={<ActivadorRecibos />} />
            <Route path="*" element={<Navigate to="/recibos" />} />
          </Routes>
        </>
      )}
    </Router>
  );
};

export default App;
