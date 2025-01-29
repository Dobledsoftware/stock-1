import React, { useEffect, useState } from "react";
import { IconButton, Snackbar, TextField } from '@mui/material';
import { Edit, Delete } from '@mui/icons-material';
import $ from "jquery";
import "datatables.net";
import "datatables.net-dt/css/jquery.datatables.min.css";

const Inventario = () => {
  const [productos, setProductos] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [openSnackbar, setOpenSnackbar] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState('');

  // Obtener inventario desde el API
  useEffect(() => {
    const obtenerInventario = async () => {
      const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/stock`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      });

      const data = await response.json();
      console.log("Datos del inventario:", data);

      if (data && Array.isArray(data)) {
        setProductos(data);
      } else {
        setProductos([]);
      }
    };

    obtenerInventario();
  }, []);

  // Inicialización de DataTable
  useEffect(() => {
    if (productos.length > 0) {
      if ($.fn.DataTable.isDataTable("#tablaInventario")) {
        $("#tablaInventario").DataTable().destroy();
      }

      $("#tablaInventario").DataTable({
        responsive: true,
        language: {
          url: "//cdn.datatables.net/plug-ins/1.13.6/i18n/es-ES.json",
        },
      });
    }
  }, [productos]);

  // Filtrar productos
  const handleSearchChange = (event) => {
    setSearchTerm(event.target.value.toLowerCase());
  };

  const filteredProductos = productos.filter((producto) =>
    producto.id_producto.toString().includes(searchTerm) ||
    producto.nombre_producto.toLowerCase().includes(searchTerm) ||
    producto.descripcion_producto.toLowerCase().includes(searchTerm) ||
    producto.codigo_barras.includes(searchTerm) ||
    producto.nombre_proveedor.toLowerCase().includes(searchTerm) ||
    producto.almacen_descripcion.toLowerCase().includes(searchTerm)
  );

  const handleEliminar = (idStock) => {
    if (window.confirm("¿Estás seguro de que deseas eliminar este stock?")) {
      console.log("Stock eliminado con ID:", idStock);
      setSnackbarMessage("Stock eliminado con éxito.");
      setOpenSnackbar(true);
    }
  };

  return (
    <>
      <div className="table-container">
        <h2>Inventario de Productos</h2>
        <TextField
          label="Buscar"
          variant="outlined"
          fullWidth
          margin="normal"
          onChange={handleSearchChange}
        />

        {/* Tabla de inventario */}
        <table id="tablaInventario" className="display">
          <thead>
            <tr>
              <th>ID Producto</th>
              <th>Nombre Producto</th>
              <th>Descripción</th>
              <th>Código de Barras</th>
              <th>Stock Actual</th>
              <th>Stock Mínimo</th>
              <th>Stock Máximo</th>
              <th>Proveedor</th>
              <th>Almacén</th>
              <th>Estante</th>
              <th>Estado</th>
              <th>Fecha Alta</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            {filteredProductos.length > 0 ? (
              filteredProductos.map((producto) => (
                <tr key={producto.id_stock}>
                  <td>{producto.id_producto}</td>
                  <td>{producto.nombre_producto}</td>
                  <td>{producto.descripcion_producto}</td>
                  <td>{producto.codigo_barras}</td>
                  <td>{producto.stock_actual}</td>
                  <td>{producto.stock_minimo}</td>
                  <td>{producto.stock_maximo || "N/A"}</td>
                  <td>{producto.nombre_proveedor}</td>
                  <td>{producto.almacen_descripcion}</td>
                  <td>{producto.descripcion_estante}</td>
                  <td>{producto.estado ? "Activo" : "Inactivo"}</td>
                  <td>{new Date(producto.fecha_alta).toLocaleString()}</td>
                  <td>
                    <IconButton
                      color="primary"
                      onClick={() => console.log("Editar", producto.id_producto)}
                    >
                      <Edit />
                    </IconButton>
                    <IconButton
                      color="error"
                      onClick={() => handleEliminar(producto.id_stock)}
                    >
                      <Delete />
                    </IconButton>
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="13">No hay productos en inventario.</td>
              </tr>
            )}
          </tbody>
        </table>
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

export default Inventario;
