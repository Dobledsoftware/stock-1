import React, { useEffect, useState } from "react";
import { IconButton, Snackbar } from "@mui/material";
import { Edit, Delete } from "@mui/icons-material";
import $ from "jquery";
import "datatables.net";
import "datatables.net-dt/css/jquery.datatables.min.css";

const TablaProductos = () => {
  const [productos, setProductos] = useState([]);
  const [marcas, setMarcas] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [openSnackbar, setOpenSnackbar] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState("");
  const [modalAbierto, setModalAbierto] = useState(false);
  const [productoEditado, setProductoEditado] = useState(null);

  useEffect(() => {
    const obtenerProductos = async () => {
      try {
        const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/productos?estado=true`);
        const data = await response.json();
        console.log("Productos obtenidos:", data);
        setProductos(data.data || []);
      } catch (error) {
        setSnackbarMessage("Error al cargar productos.");
        setOpenSnackbar(true);
      }
    };
    obtenerProductos();
  }, []);

  useEffect(() => {
    const obtenerMarcas = async () => {
      try {
        const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/producto_marcas?estado=true`);
        const data = await response.json();
        setMarcas(data.data || []);
      } catch (error) {
        console.error("Error al obtener marcas:", error);
      }
    };
    obtenerMarcas();
  }, []);

  useEffect(() => {
    if (productos.length > 0) {
      if ($.fn.DataTable.isDataTable("#tablaProductos")) {
        $("#tablaProductos").DataTable().destroy();
      }
      $("#tablaProductos").DataTable({
        responsive: true,
        language: {
          url: "//cdn.datatables.net/plug-ins/1.13.6/i18n/es-ES.json",
        },
      });
    }
  }, [productos]);

  const handleEditar = (producto) => {
    setProductoEditado({
      ...producto,
      producto_marca: producto.producto_marca_id || "",
    });
    setModalAbierto(true);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/producto`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ accion: "editarProducto", ...productoEditado }),
      });
      if (!response.ok) throw new Error("Error al editar el producto");

      setSnackbarMessage("Producto editado con éxito.");
      setProductos((prev) =>
        prev.map((p) => (p.producto_id === productoEditado.producto_id ? productoEditado : p))
      );
      setModalAbierto(false);
    } catch (error) {
      setSnackbarMessage("Error al guardar cambios.");
    } finally {
      setOpenSnackbar(true);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setProductoEditado((prev) => ({ ...prev, [name]: value }));
  };

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
              <th>Precio venta ARS</th>
              <th>Precio venta USD</th>
              <th>Marca</th>
              <th>Código de Barra</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            {productos.map((producto) => (
              <tr key={producto.producto_id}>
                <td>{producto.producto_id}</td>
                <td>{producto.producto_nombre}</td>
                <td>{producto.producto_descripcion}</td>
                <td>{producto.precio_venta_ars}</td>
                <td>{producto.precio_venta_usd}</td>
                <td>{producto.producto_marca}</td>
                <td>{producto.producto_codigo_barras || "N/A"}</td>
                <td>
                  <IconButton color="primary" onClick={() => handleEditar(producto)}>
                    <Edit />
                  </IconButton>
                  <IconButton color="error">
                    <Delete />
                  </IconButton>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {modalAbierto && (
        <div className="modal">
          <div className="modal-content">
            <h3>Editar Producto</h3>
            <form onSubmit={handleSubmit}>
              <input type="text" name="producto_nombre" placeholder="Nombre" value={productoEditado?.producto_nombre || ""} onChange={handleInputChange} required />
              <input type="text" name="producto_descripcion" placeholder="Descripción" value={productoEditado?.producto_descripcion || ""} onChange={handleInputChange} required />
              <input type="number" name="precio_venta_ars" placeholder="Precio de venta ARS" value={productoEditado?.precio_venta_ars || ""} onChange={handleInputChange} required />
              <input type="number" name="precio_venta_usd" placeholder="Precio de venta USD" value={productoEditado?.precio_venta_usd || ""} onChange={handleInputChange} required />
              <input type="text" name="producto_codigo_barras" placeholder="Código de Barras" value={productoEditado?.producto_codigo_barras || ""} onChange={handleInputChange} required />
              <select name="producto_marca" value={productoEditado?.producto_marca || ""} onChange={handleInputChange} required>
                <option value="">Seleccione una marca</option>
                {marcas.map((marca) => (
                  <option key={marca.id_marca} value={marca.id_marca}>{marca.descripcion}</option>
                ))}
              </select>
              <button type="submit">Guardar Cambios</button>
              <button type="button" onClick={() => setModalAbierto(false)}>Cancelar</button>
            </form>
          </div>
        </div>
      )}
    </>
  );
};

export default TablaProductos;