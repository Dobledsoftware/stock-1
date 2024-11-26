import { useState } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Login from './Login';
import Navbar from './Navbar';
import Recibos from './Recibos';
import Usuarios from './Usuarios';
import MisDatos from './MisDatos';
import ActivadorRecibos from './ActivadorRecibos';
import '../styles/global.css'; // Estilos personalizados de la tabla

const App = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  const handleLogin = (identifier, password, method) => {
    console.log(`Attempting login via ${method}`);
    if (method === 'LDAP') {
      // Lógica de autenticación LDAP
      console.log(`LDAP login for samAccountName: ${identifier}`);
    } else {
      // Lógica de autenticación API
      console.log(`API login for CUIL: ${identifier}`);
    }

    // Simula un inicio de sesión exitoso
    setIsAuthenticated(true);
  };

  const handleLogout = () => {
    console.log('Cerrar sesión');
    setIsAuthenticated(false); // Maneja el cierre de sesión
  };

  return (
    <Router>
      {isAuthenticated ? (
        <>
          <Navbar onLogout={handleLogout} />
          <Routes>
            <Route path="/recibos" element={<Recibos />} />
            <Route path="/usuarios" element={<Usuarios />} />
            <Route path="/mis-datos" element={<MisDatos />} />
            <Route path="/activador-recibos" element={<ActivadorRecibos />} />
          </Routes>
        </>
      ) : (
        <Login onLogin={handleLogin} /> // Pasamos la función de login
      )}
    </Router>
  );
};


export default App;
