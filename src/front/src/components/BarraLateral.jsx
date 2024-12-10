import React, { useState } from "react";
import { Link } from "react-router-dom";

const BarraLateral = () => {
  // Estados para controlar los menús desplegables
  const [perfilVisible, setPerfilVisible] = useState(false);
  const [stockVisible, setStockVisible] = useState(false);
  const [ventasVisible, setVentasVisible] = useState(false);

  // Simulando datos del usuario
  const usuario = {
    nombre: "Juan Pérez",
    correo: "juan.perez@example.com",
  };

  // Maneja la visibilidad de los menús desplegables
  const togglePerfil = () => {
    setPerfilVisible(!perfilVisible);
  };

  const toggleStock = () => {
    setStockVisible(!stockVisible);
  };

  const toggleVentas = () => {
    setVentasVisible(!ventasVisible);
  };

  return (
    <div className="barra-lateral">
      <div className="logo">
        <h2>Sistema Stock</h2>
      </div>
      <nav>
        <ul>
          <li>
            <div className="menu-desplegable" onClick={toggleStock}>
              <span>Stock</span>
              {stockVisible && (
                <ul className="dropdown">
                  <li><Link to="/inventario">Inventario</Link></li>
                  <li><Link to="/movimientos">Movimientos</Link></li>
                  <li><Link to="/ajustes">Ajustes</Link></li>
                </ul>
              )}
            </div>
          </li>
          <li>
            <div className="menu-desplegable" onClick={toggleVentas}>
              <span>Ventas</span>
              {ventasVisible && (
                <ul className="dropdown">
                  <li><Link to="/ventas">Ventas</Link></li>
                  <li><Link to="/devoluciones">Devoluciones</Link></li>
                  <li><Link to="/consultas">Consultas</Link></li>
                </ul>
              )}
            </div>
          </li>
          <li>
            <Link to="/administracion">
              <span>Administración</span>
            </Link>
          </li>
          <li>
            <div className="perfil" onClick={togglePerfil}>
              <span>Perfil</span>
              {perfilVisible && (
                <ul className="dropdown">
                  <li><strong>{usuario.nombre}</strong></li>
                  <li>{usuario.correo}</li>
                  <li><Link to="/editar-perfil">Editar Perfil</Link></li>
                  <li><Link to="/cambiar-contrasena">Cambiar Contraseña</Link></li>
                </ul>
              )}
            </div>
          </li>
          <li>
            <button className="boton-salir">
              <span>Salir</span>
            </button>
          </li>
        </ul>
      </nav>
    </div>
  );
};

export default BarraLateral;
