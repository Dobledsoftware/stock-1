import React, { useState } from 'react';
import '../styles/Header.css'; // Asegúrate de tener un archivo CSS para los estilos

function Header() {
  const [dropdownVisible, setDropdownVisible] = useState(false);

  const toggleDropdown = () => {
    setDropdownVisible(!dropdownVisible);
  };

  return (
    <header className="header">
      <div className="logo">
        <img src="../public/img/imagen.jpg" alt="Logo" className="logo-img" />
      </div>
      <div className="usuario">
        <button className="usuario-boton" onClick={toggleDropdown}>
          Usuario <span className="usuario-icono">▼</span>
        </button>
        {dropdownVisible && (
          <div className="dropdown">
            <ul>
              <li>Perfil</li>
              <li>Cerrar sesión</li>
            </ul>
          </div>
        )}
      </div>
    </header>
  );
}

export default Header;
