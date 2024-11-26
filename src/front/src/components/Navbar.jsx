// eslint-disable-next-line no-unused-vars
import React from 'react';
import { NavLink } from 'react-router-dom';
import PropTypes from 'prop-types';
import '../styles/Navbar.css'; // Crea este archivo para estilos específicos de Navbar

const Navbar = ({ onLogout }) => {
  return (
    <nav className="navbar">
      <ul className="nav-list">
        <br />
        <li className="nav-item">
          <NavLink to="/recibos" className="nav-link" activeClassName="active">
            Mi tabla de recibos
          </NavLink>
        </li>
        <li className="nav-item">
          <NavLink to="/usuarios" className="nav-link" activeClassName="active">
            Tabla de usuarios
          </NavLink>
        </li>
        <li className="nav-item">
          <NavLink to="/mis-datos" className="nav-link" activeClassName="active">
            Mis datos
          </NavLink>
        </li>
        <li className="nav-item">
          <NavLink to="/activador-recibos" className="nav-link" activeClassName="active">
            Activador de recibos
          </NavLink>
        </li>
        <li className="nav-item">
          <button onClick={onLogout} className="logout-button">
            Cerrar Sesión
          </button>
        </li>
      </ul>
    </nav>
  );
};



Navbar.propTypes = {
  onLogout: PropTypes.func.isRequired,
};

export default Navbar;
