import React, { useEffect, useState } from "react";
import { IconButton, Snackbar, Alert } from "@mui/material";
import { Edit, Delete } from "@mui/icons-material";
import $ from "jquery";
import "datatables.net";
import "datatables.net-dt/css/jquery.datatables.min.css";
import '../styles/TablaProductos2.css';

const TablaProductos = () => {
  const baseUrl = import.meta.env.VITE_API_BASE_URL;
  const [productos, setProductos] = useState([]);
  const [marcas, setMarcas] = useState([]);
  const [openSnackbar, setOpenSnackbar] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState("");
  const [snackbarSeverity, setSnackbarSeverity] = useState("info");
  const [modalAbierto, setModalAbierto] = useState(false);
  const [productoEditado, setProductoEditado] = useState(null);

  useEffect(() => {
    fetchData(`${baseUrl}/productos?estado=true`, setProductos);
    fetchData(`${baseUrl}/producto_marcas?estado=true`, setMarcas);
  }, [baseUrl]);

  useEffect(() => {
    if (productos.length > 0) {
      if ($.fn.DataTable.isDataTable("#tablaProductos")) {
        $("#tablaProductos").DataTable().destroy();
      }
      $("#tablaProductos").DataTable({
        responsive: true,
        language: { url: "//cdn.datatables.net/plug-ins/1.13.6/i18n/es-ES.json" },
      });
    }
  }, [productos]);

  const fetchData = async (url, setter) => {
    try {
      const response = await fetch(url);
      const data = await response.json();
      setter(data.data || []);
    } catch (error) {
      mostrarSnackbar(`Error al cargar datos: ${error.message}`, "error");
    }
  };

  const mostrarSnackbar = (message, severity = "info") => {
    setSnackbarMessage(message);
    setSnackbarSeverity(severity);
    setOpenSnackbar(true);
  };

  const handleEditar = (producto) => {
    setProductoEditado({
      producto_id: producto.producto_id,
      nombre: producto.producto_nombre || "",
      descripcion: producto.producto_descripcion || "",
      precio_venta_ars: producto.precio_venta_ars || 0,
      precio_venta_usd: producto.precio_venta_usd || 0,
      codigo_barras: producto.producto_codigo_barras || "",
      id_marca: producto.producto_marca || "",
      aplicar_incremento_automatico_ars: producto.aplicar_incremento_automatico_ars || false,
      aplicar_incremento_automatico_usd: producto.aplicar_incremento_automatico_usd || false,
      es_dolar: producto.es_dolar || false,
    });
    setModalAbierto(true);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(`${baseUrl}/producto`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(productoEditado),
      });

      if (!response.ok) throw new Error("Error al editar el producto");

      mostrarSnackbar("Producto editado con éxito.", "success");
      setProductos((prev) =>
        prev.map((p) => (p.producto_id === productoEditado.producto_id ? productoEditado : p))
      );
      setModalAbierto(false);
    } catch (error) {
      mostrarSnackbar("Error al guardar cambios.", "error");
    }
  };

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setProductoEditado((prev) => ({
      ...prev,
      [name]: type === "checkbox" ? checked : value,
    }));
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
              <th>Precio ARS</th>
              <th>Precio USD</th>
              <th>Marca</th>
              <th>Código de Barras</th>
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
                <td>{producto.producto_marca || "Sin marca"}</td>
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
            <form onSubmit={handleSubmit} className="form-container">
              <div className="form-group">
                <label>Nombre</label>
                <input type="text" name="nombre" value={productoEditado?.nombre || ""} onChange={handleInputChange} required className="input-field" />
              </div>

              <div className="form-group">
                <label>Descripción</label>
                <input type="text" name="descripcion" value={productoEditado?.descripcion || ""} onChange={handleInputChange} required className="input-field" />
              </div>

              <div className="form-group">
                <label>Precio de Venta ARS</label>
                <input type="number" name="precio_venta_ars" value={productoEditado?.precio_venta_ars || 0} onChange={handleInputChange} required className="input-field" />
              </div>

              <div className="form-group">
                <label>Precio de Venta USD</label>
                <input type="number" name="precio_venta_usd" value={productoEditado?.precio_venta_usd || 0} onChange={handleInputChange} required className="input-field" />
              </div>

              <div className="form-group">
                <label>Código de Barras</label>
                <input type="text" name="codigo_barras" value={productoEditado?.codigo_barras || ""} onChange={handleInputChange} required className="input-field" />
              </div>

              <div className="form-group">
                <label>Marca</label>
                <select name="id_marca" value={productoEditado?.id_marca || ""} onChange={handleInputChange} required className="select-field">
                  <option value="">Seleccione una marca</option>
                  {marcas.map((marca) => (
                    <option key={marca.id_marca} value={marca.id_marca}>
                      {marca.descripcion}
                    </option>
                  ))}
                </select>
              </div>

              <div className="checkbox-group">
                <label><input type="checkbox" name="aplicar_incremento_automatico_ars" checked={productoEditado?.aplicar_incremento_automatico_ars} onChange={handleInputChange} /> Aplicar incremento automático ARS</label>
                <label><input type="checkbox" name="aplicar_incremento_automatico_usd" checked={productoEditado?.aplicar_incremento_automatico_usd} onChange={handleInputChange} /> Aplicar incremento automático USD</label>
                <label><input type="checkbox" name="es_dolar" checked={productoEditado?.es_dolar} onChange={handleInputChange} /> Producto en dólares</label>
              </div>

              <div className="button-group">
                <button type="submit" className="submit-button">Guardar Cambios</button>
                <button type="button" onClick={() => setModalAbierto(false)} className="cancel-button">Cancelar</button>
              </div>
            </form>
          </div>
        </div>
      )}

      <Snackbar open={openSnackbar} autoHideDuration={3000} onClose={() => setOpenSnackbar(false)}>
        <Alert onClose={() => setOpenSnackbar(false)} severity={snackbarSeverity}>{snackbarMessage}</Alert>
      </Snackbar>
    </>
  );
};

export default TablaProductos;
