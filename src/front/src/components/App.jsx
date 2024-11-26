import { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { SnackbarProvider } from 'notistack'; // Importar Notistack
import Login from './Login';
import Navbar from './Navbar';
import Recibos from './Recibos';
import Usuarios from './Usuarios';
/* import MisDatos from './MisDatos'; */
import Carga from './carga'; // Asegúrate de que la importación sea correcta
import ActivadorRecibos from './ActivadorRecibos';
import '../styles/global.css'; // Estilos personalizados de la tabla

const App = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [userRole, setUserRole] = useState(null); // Estado para almacenar el rol del usuario

  // Verificar la autenticación y el rol al cargar el componente
  useEffect(() => {
    const token = localStorage.getItem('auth_token'); // Corrige el nombre del token aquí
    const role = localStorage.getItem('rol'); // Obtener el rol del usuario
    if (token) {
      setIsAuthenticated(true); // Si hay un token, consideramos que está autenticado
      setUserRole(role); // Almacenar el rol en el estado
    }
    console.log(`Estado de autenticación: ${isAuthenticated}`);
    console.log(`Rol del usuario: ${role}`); // Verifica qué rol se está obteniendo
  }, [isAuthenticated]);

  const handleLogin = (token) => {
    console.log(`User logged in with token: ${token}`);
    setIsAuthenticated(true);
    const role = localStorage.getItem('rol'); // Obtener el rol del usuario
    setUserRole(role); // Establecer el rol en el estado
    console.log(`Rol guardado en localStorage: ${role}`); // Verifica qué rol se ha guardado
  };

  const handleLogout = () => {
    console.log('Cerrar sesión');
    localStorage.clear(); // Limpiar todo el localStorage
    setIsAuthenticated(false); // Manejar el cierre de sesión
    setUserRole(null); // Reiniciar el rol del usuario
  };

  return (
    <SnackbarProvider maxSnack={3}> {/* Envolver la app con SnackbarProvider */}
      <Router>
        {isAuthenticated ? (
          <>
            <Navbar onLogout={handleLogout} />
            <Routes>
              {/* Mostrar Recibos y MisDatos para todos los usuarios autenticados */}
              <Route path="/recibos" element={<Recibos />} />
             {/*  <Route path="/mis-datos" element={<MisDatos />} /> */}
              {/* Mostrar Usuarios solo para rol 2 */}
              {userRole === '2' && ( // Asegúrate de que el rol sea un string '2'
                <Route path="/usuarios" element={<Usuarios />} />
              )}
              {/* Rutas adicionales que todos pueden acceder */}
              <Route path="/activador-recibos" element={<ActivadorRecibos />} />
              <Route path="/carga" element={<Carga />} />
              {/* Ruta por defecto o página de error para usuarios que no tienen acceso */}
              <Route path="*" element={<h2>No tienes acceso a esta sección</h2>} />
            </Routes>
          </>
        ) : (
          <Login onLogin={handleLogin} />
        )}
      </Router>
    </SnackbarProvider>
  );
};

export default App;
