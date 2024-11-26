// eslint-disable-next-line no-unused-vars
import React from 'react';
import { NavLink } from 'react-router-dom';
import PropTypes from 'prop-types';
import '../styles/Navbar.css'; // Crea este archivo para estilos específicos de Navbar

const Navbar = ({ onLogout }) => {
  const userRole = localStorage.getItem('rol'); // Obtener el rol del usuario desde localStorage

  return (
    <nav className="navbar">
      <img src="/public/img/logo.png" alt="Logo" className="logo" />
      <ul className="nav-list">
        {/* Mostrar enlaces según el rol del usuario */}
        {userRole === '1' && ( // Mostrar solo para rol 1
          <>
            {/* Enlaces para rol 1 */}
          </>
        )}
        {userRole === '2' && ( // Mostrar para rol 2
          <>
            <li className="nav-item">
              <NavLink to="/usuarios" className="nav-link" activeClassName="active">
                Tabla de usuarios
              </NavLink>
            </li>
            <li className="nav-item">
              <NavLink to="/recibos" className="nav-link" activeClassName="active">
                Mi tabla de recibos
              </NavLink>
            </li>
            <li className="nav-item">
              <NavLink to="/activador-recibos" className="nav-link" activeClassName="active">
                Activador de recibos
              </NavLink>
            </li>
            <li className="nav-item">
              <NavLink to="/carga" className="nav-link" activeClassName="active">
                Carga
              </NavLink>
            </li>
          </>
        )}
      </ul>
      <button onClick={onLogout} className="logout-button">
        Cerrar Sesión
      </button>
    </nav>
  );
};

Navbar.propTypes = {
  onLogout: PropTypes.func.isRequired,
};

export default Navbar;
