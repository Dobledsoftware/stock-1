import React, { useEffect, useState } from "react";
import $ from "jquery";
import "datatables.net";
import "datatables.net-dt/css/jquery.datatables.min.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faEdit, faTrash } from "@fortawesome/free-solid-svg-icons";

const TablaProductos = () => {
  const [productos, setProductos] = useState([]);

  const handleEliminar = (idProducto) => {
    if (window.confirm("¿Estás seguro de que deseas eliminar este producto?")) {
      console.log("Producto eliminado con ID:", idProducto);
      // Aquí se llamaría al backend para eliminar el producto
    }
  };

  useEffect(() => {
    const obtenerProductos = async () => {
      const response = await fetch(
        `${import.meta.env.VITE_API_BASE_URL}/producto`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            accion: "verTodosLosProductos",
            estado: "Activo",
          }),
        }
      );
      const data = await response.json();
      setProductos(data.data || []);
    };

    obtenerProductos();
  }, []);

  useEffect(() => {
    if (productos.length > 0) {
      // Destruir la tabla si ya está inicializada para evitar duplicados
      if ($.fn.DataTable.isDataTable("#tablaProductos")) {
        $("#tablaProductos").DataTable().destroy();
      }

      // Inicializar DataTable
      $("#tablaProductos").DataTable({
        responsive: true,
        language: {
          url: "//cdn.datatables.net/plug-ins/1.13.6/i18n/es-ES.json",
        },
      });
    }
  }, [productos]);

  return (
    <div>
      <h2>Lista de Productos</h2>
      <div style={{ overflowX: "auto" }}>
        <table id="tablaProductos" className="display">
          <thead>
            <tr>
              <th>ID</th>
              <th>Nombre</th>
              <th>Descripción</th>
              <th>Precio</th>
              <th>Marca</th>
              <th>Codigo de barra</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            {productos.map((producto) => (
              <tr key={producto.producto_id}>
                <td>{producto.producto_id}</td>
                <td>{producto.producto_nombre}</td>
                <td>{producto.producto_descripcion}</td>
                <td>{producto.producto_precio}</td>
                <td>{producto.producto_marca}</td>
                <td>{producto.producto_codigo_barras || "N/A"}</td>
                <td>
                  <button
                    onClick={() =>
                      console.log("Editar producto con ID:", producto.producto_id)
                    }
                    title="Editar"
                    className="icon-button"
                  >
                    <FontAwesomeIcon icon={faEdit} />
                  </button>
                  <button
                    onClick={() => handleEliminar(producto.producto_id)}
                    title="Eliminar"
                    className="icon-button"
                  >
                    <FontAwesomeIcon icon={faTrash} />
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default TablaProductos;
