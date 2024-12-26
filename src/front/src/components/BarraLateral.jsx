import React, { useState } from "react";
import { NavLink, useLocation } from "react-router-dom";
import '../styles/barraLateral.css';

const BarraLateral = () => {
  const [activeItem, setActiveItem] = useState(null);
  const location = useLocation();

  // Simulando datos del usuario
  const usuario = {
    nombre: "Juan Pérez",
    correo: "juan.perez@example.com",
  };

  // Función para manejar la selección de un ítem
  const handleActiveItem = (item) => {
    setActiveItem(activeItem === item ? null : item);  // Alterna entre activo y no activo
  };

  return (
    <div className="barra-lateral">
      <div className="logo-container">
        <img src="../public/img/imagen.jpg" alt="logo" className="logo" /> 
      </div>
      
      <nav>
        <ul>
          <li className={activeItem === "stock" || location.pathname.includes("/inventario") || location.pathname.includes("/almacen") || location.pathname.includes("/panel") ? "active" : ""}>
            <div className="menu-desplegable" onClick={() => handleActiveItem("stock")}>
              <i className="icono fa fa-archive"></i> Stock
            </div>
            {activeItem === "stock" && (
              <ul className="dropdown">
                <li><NavLink to="/stock">Inventario</NavLink></li>
                <li><NavLink to="/config">Configuracion de producto</NavLink></li>
                <li><NavLink to="/abastecimiento">Abastecimiento</NavLink></li>
                <li><NavLink to="/panel">Panel</NavLink></li>
              </ul>
            )}
          </li>
          <li className={activeItem === "ventas" || location.pathname.includes("/nueva-venta") || location.pathname.includes("/historico-ventas") ? "active" : ""}>
            <div className="menu-desplegable" onClick={() => handleActiveItem("ventas")}>
              <i className="icono fa fa-shopping-cart"></i> Ventas
            </div>
            {activeItem === "ventas" && (
              <ul className="dropdown">
                <li><NavLink to="/ventas">Nueva Venta</NavLink></li>
                <li><NavLink to="/cierre">Cierre de Caja</NavLink></li>
              </ul>
            )}
          </li>
          <li className={activeItem === "administracion" || location.pathname.includes("/usuarios") || location.pathname.includes("/configuracion") ? "active" : ""}>
            <div className="menu-desplegable" onClick={() => handleActiveItem("administracion")}>
              <i className="icono fa fa-cogs"></i> Administración
            </div>
            {activeItem === "administracion" && (
              <ul className="dropdown">
                <li><NavLink to="/administracion">Usuarios</NavLink></li>
                <li><NavLink to="/configuracion">Configuración</NavLink></li>
              </ul>
            )}
          </li>
          <li className={activeItem === "perfil" || location.pathname.includes("/editar-perfil") || location.pathname.includes("/cambiar-contrasena") ? "active" : ""}>
            <div className="menu-desplegable" onClick={() => handleActiveItem("perfil")}>
              <i className="icono fa fa-user"></i> Perfil
            </div>
            {activeItem === "perfil" && (
              <ul className="dropdown">
                <li><NavLink to="/editar-perfil">Editar Perfil</NavLink></li>
                <li><NavLink to="/cambiar-contrasena">Cambiar Contraseña</NavLink></li>
              </ul>
            )}
          </li>
          <li>
            <button className="boton-salir">
              <i className="icono fa fa-sign-out-alt"></i> Salir
            </button>
          </li>
        </ul>
      </nav>
    </div>
  );
};

export default BarraLateral;
