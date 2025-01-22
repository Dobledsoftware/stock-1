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
      const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/tabla_stock`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({}), // Pasar objeto vacío
      });

      const data = await response.json();
      console.log("Datos del inventario:", data); // Verifica qué llega aquí

      // Verifica si la respuesta tiene los datos y setea el estado correctamente
      if (data && data.length > 0) {
        setProductos(data); // Asegúrate de que la respuesta sea un array
      } else {
        setProductos([]); // En caso de que no haya datos
      }
    };

    obtenerInventario();
  }, []);

  // Inicialización de DataTable y actualización de la tabla
  useEffect(() => {
    if (productos.length > 0) {
      // Destruir la tabla si ya está inicializada para evitar duplicados
      if ($.fn.DataTable.isDataTable("#tablaInventario")) {
        $("#tablaInventario").DataTable().destroy();
      }

      // Inicializar DataTable
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
    producto.stock_actual.toString().includes(searchTerm) ||
    producto.stock_minimo.toString().includes(searchTerm) ||
    producto.stock_maximo.toString().includes(searchTerm)
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

        {/* Tabla de inventario */}
        <table id="tablaInventario" className="display">
          <thead>
            <tr>
              <th>ID Producto</th>
              <th>Stock Actual</th>
              <th>Stock Mínimo</th>
              <th>Stock Máximo</th>
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
                  <td>{producto.stock_actual}</td>
                  <td>{producto.stock_minimo}</td>
                  <td>{producto.stock_maximo || "N/A"}</td>
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
                <td colSpan="7">No hay productos en inventario.</td>
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
