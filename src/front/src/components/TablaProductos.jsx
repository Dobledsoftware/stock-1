import React, { useEffect, useState } from "react";
import { Button, IconButton, TextField, Snackbar } from '@mui/material';
import { Edit, Delete } from '@mui/icons-material';
import $ from "jquery";
import "datatables.net";
import "datatables.net-dt/css/jquery.datatables.min.css";

const TablaProductos = () => {
  const [productos, setProductos] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [openSnackbar, setOpenSnackbar] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState('');
  
  useEffect(() => {
    const obtenerProductos = async () => {
      const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/producto`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          accion: "verTodosLosProductos",
          estado: "Activo",
        }),
      });
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

  const handleEliminar = (idProducto) => {
    if (window.confirm("¿Estás seguro de que deseas eliminar este producto?")) {
      console.log("Producto eliminado con ID:", idProducto);
      setSnackbarMessage("Producto eliminado con éxito.");
      setOpenSnackbar(true);
    }
  };

  const handleSearchChange = (event) => {
    setSearchTerm(event.target.value.toLowerCase());
  };

  const filteredProductos = productos.filter((producto) =>
    producto.producto_nombre.toLowerCase().includes(searchTerm)
  );

  return (
    <>
      <div className="table-container">
        <h2>Lista de Productos</h2>
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
            {filteredProductos.map((producto) => (
              <tr key={producto.producto_id}>
                <td>{producto.producto_id}</td>
                <td>{producto.producto_nombre}</td>
                <td>{producto.producto_descripcion}</td>
                <td>{producto.producto_precio}</td>
                <td>{producto.producto_marca}</td>
                <td>{producto.producto_codigo_barras || "N/A"}</td>
                <td>
                  <IconButton
                    color="primary"
                    onClick={() => console.log("Editar", producto.producto_id)}
                  >
                    <Edit />
                  </IconButton>
                  <IconButton
                    color="error"
                    onClick={() => handleEliminar(producto.producto_id)}
                  >
                    <Delete />
                  </IconButton>
                </td>
              </tr>
            ))}
          </tbody>
        </table>

        {/* Paginación con MUI */}
        {/* Agregar la paginación aquí si es necesario */}
      </div>

      {/* Snackbar de notificación */}
      <Snackbar
        open={openSnackbar}
        autoHideDuration={3000}
        onClose={() => setOpenSnackbar(false)}
        message={snackbarMessage}
      />
    </>
  );
};

export default TablaProductos;
