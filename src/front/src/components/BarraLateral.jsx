import React, { useState } from "react";
import { NavLink, useLocation } from "react-router-dom";
import "../styles/barraLateral.css";

const BarraLateral = () => {
  const [activeItem, setActiveItem] = useState(null);
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const location = useLocation();

  // Datos del usuario simulados
  const usuario = {
    nombre: "Juan Pérez",
    correo: "juan.perez@example.com",
  };

  // Alternar elemento activo
  const handleActiveItem = (item) => {
    setActiveItem(activeItem === item ? null : item);
  };

  // Alternar barra lateral
  const toggleSidebar = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };

  return (
    <div className={`barra-lateral ${isSidebarOpen ? "open" : "closed"}`}>
      {/* Logo y botón hamburguesa */}
      <div className="logo-container">
  <img
    src="../public/img/imagen.jpg"
    alt="logo"
    className="logo"
    onClick={toggleSidebar} // Añadimos la función al hacer clic sobre el logo
  />
</div>


      {/* Menú de navegación */}
      <nav>
        <ul>
          {/* Menú Stock */}
          <li className={activeItem === "stock" ? "active" : ""}>
            <div
              className="menu-desplegable"
              onClick={() => {
                if (!isSidebarOpen) setIsSidebarOpen(true);
                handleActiveItem("stock");
              }}
            >
              <i className="icono fa fa-archive"></i>
              {isSidebarOpen && "Stock"}
            </div>
            {activeItem === "stock" && isSidebarOpen && (
              <ul className="dropdown">
                <li><NavLink to="/inventario">Inventario</NavLink></li>
                <li><NavLink to="/movimientos">Stock</NavLink></li>
                <li><NavLink to="/config">Configuración de producto</NavLink></li>
                <li><NavLink to="/abastecimiento">Abastecimiento</NavLink></li>
                <li><NavLink to="/productos">Productos</NavLink></li>
                <li><NavLink to="/panel">Panel</NavLink></li>
              </ul>
            )}
          </li>

          {/* Menú Ventas */}
          <li className={activeItem === "ventas" ? "active" : ""}>
            <div
              className="menu-desplegable"
              onClick={() => {
                if (!isSidebarOpen) setIsSidebarOpen(true);
                handleActiveItem("ventas");
              }}
            >
              <i className="icono fa fa-shopping-cart"></i>
              {isSidebarOpen && "Ventas"}
            </div>
            {activeItem === "ventas" && isSidebarOpen && (
              <ul className="dropdown">
                <li><NavLink to="/ventas">Nueva Venta</NavLink></li>
                <li><NavLink to="/cierre">Cierre de Caja</NavLink></li>
              </ul>
            )}
          </li>

          {/* Menú Administración */}
          <li className={activeItem === "administracion" ? "active" : ""}>
            <div
              className="menu-desplegable"
              onClick={() => {
                if (!isSidebarOpen) setIsSidebarOpen(true);
                handleActiveItem("administracion");
              }}
            >
              <i className="icono fa fa-cogs"></i>
              {isSidebarOpen && "Administración"}
            </div>
            {activeItem === "administracion" && isSidebarOpen && (
              <ul className="dropdown">
                <li><NavLink to="/administracion">Usuarios</NavLink></li>
                <li><NavLink to="/configuracion">Configuración</NavLink></li>
              </ul>
            )}
          </li>

          {/* Menú Perfil */}
          <li className={activeItem === "perfil" ? "active" : ""}>
            <div
              className="menu-desplegable"
              onClick={() => {
                if (!isSidebarOpen) setIsSidebarOpen(true);
                handleActiveItem("perfil");
              }}
            >
              <i className="icono fa fa-user"></i>
              {isSidebarOpen && "Perfil"}
            </div>
            {activeItem === "perfil" && isSidebarOpen && (
              <ul className="dropdown">
                <li><NavLink to="/editar-perfil">Editar Perfil</NavLink></li>
                <li><NavLink to="/cambiar-contrasena">Cambiar Contraseña</NavLink></li>
              </ul>
            )}
          </li>

          {/* Salir */}
          <li>
            <button className="boton-salir">
              <i className="icono fa fa-sign-out-alt"></i>
              {isSidebarOpen && "Salir"}
            </button>
          </li>
        </ul>
      </nav>
    </div>
  );
};

export default BarraLateral;
