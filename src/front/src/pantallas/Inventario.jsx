import React, { useEffect, useState, useMemo, useRef } from "react";
import { 
  IconButton, TextField, Dialog, DialogTitle, DialogContent, DialogActions, Button, 
  Grid, InputAdornment 
} from "@mui/material";
import { Edit, FilterList, Search, Close } from "@mui/icons-material";

const Inventario = () => {
  const [productos, setProductos] = useState([]);
  const [filters, setFilters] = useState({
    id_producto: "",
    nombre_producto: "",
    descripcion_producto: "",
    codigo_barras: "",
    stock_actual: "",
    almacen_descripcion: "",
    descripcion_estante: "",
    fecha_ingreso: "",
  });

  const [openFilters, setOpenFilters] = useState(false);
  const [tempFilters, setTempFilters] = useState(filters);
  const codigoBarrasRef = useRef(null);

  // Obtener inventario desde la API
  useEffect(() => {
    const obtenerInventario = async () => {
      try {
        const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/inventario`);
        const data = await response.json();
        console.log("Datos del inventario:", data);
        setProductos(Array.isArray(data) ? data : []);
      } catch (error) {
        console.error("Error obteniendo inventario:", error);
      }
    };
    obtenerInventario();
  }, []);

  // Enfocar automáticamente el campo de Código de Barras cuando se abre el modal
  useEffect(() => {
    if (openFilters && codigoBarrasRef.current) {
      codigoBarrasRef.current.focus();
    }
  }, [openFilters]);

  // Filtrado en React con useMemo
  const filteredProductos = useMemo(() => {
    return productos.filter((producto) =>
      Object.entries(filters).every(([key, value]) =>
        !value ? true : producto[key]?.toString().toLowerCase().includes(value.toLowerCase())
      )
    );
  }, [productos, filters]);

  // Manejo de cambios en filtros (sin afectar la tabla en tiempo real)
  const handleTempFilterChange = (event) => {
    setTempFilters((prev) => ({
      ...prev,
      [event.target.name]: event.target.value,
    }));
  };

  // Aplicar filtros al cerrar el modal
  const applyFilters = () => {
    setFilters(tempFilters);
    setOpenFilters(false);
  };

  // Limpiar filtros y cerrar modal
  const resetFilters = () => {
    setTempFilters({
      id_producto: "",
      nombre_producto: "",
      descripcion_producto: "",
      codigo_barras: "",
      stock_actual: "",
      almacen_descripcion: "",
      descripcion_estante: "",
      fecha_ingreso: "",
    });
    setFilters({
      id_producto: "",
      nombre_producto: "",
      descripcion_producto: "",
      codigo_barras: "",
      stock_actual: "",
      almacen_descripcion: "",
      descripcion_estante: "",
      fecha_ingreso: "",
    });
    setOpenFilters(false);
  };

  return (
    <>
      <div className="table-container">
        <h2>Inventario de Productos</h2>

        {/* Botón de filtro sobre la tabla */}
        <div style={{ display: "flex", justifyContent: "flex-start", marginBottom: "15px" }}>
          <Button
            variant="contained"
            color="primary"
            startIcon={<FilterList />}
            onClick={() => {
              setTempFilters(filters);
              setOpenFilters(true);
            }}
          >
            Filtros
          </Button>
        </div>

        {/* Ventana emergente de filtros */}
        <Dialog 
          open={openFilters} 
          onClose={() => setOpenFilters(false)}
          fullWidth
          maxWidth="md"
        >
          <DialogTitle 
            sx={{ 
              background: "linear-gradient(45deg, #007AFF, #00B4D8)", 
              color: "white", 
              textAlign: "center",
              fontWeight: "bold",
              padding: "5px 20px", fontSize: "1.2rem",
            }}
          >
            Filtrar Productos
          </DialogTitle>
          
          <DialogContent sx={{ padding: "30px", background: "#f5f5f5", marginTop: "10px" }}>
            <Grid container spacing={2}>
              {Object.keys(tempFilters).map((field) => (
                <Grid item xs={12} sm={6} md={4} key={field}>
                  <TextField
  sx={{ marginTop: "10px" }}
  fullWidth
  label={field.replace("_", " ").toUpperCase()}
  name={field}
  variant="outlined"
  size="small"
  type={field === "fecha_ingreso" ? "date" : "text"}
  value={tempFilters[field]}
  onChange={handleTempFilterChange}
  inputRef={field === "codigo_barras" ? codigoBarrasRef : null}
  InputLabelProps={field === "fecha_ingreso" ? { shrink: true } : {}}  // ✅ Evita que el label se superponga
  InputProps={{
    startAdornment: field !== "fecha_ingreso" ? (
      <InputAdornment position="start">
        <Search />
      </InputAdornment>
    ) : null,
  }}
/>

                </Grid>
              ))}
            </Grid>
          </DialogContent>

          <DialogActions sx={{ background: "#f5f5f5", padding: "15px", justifyContent: "center" }}>
            <Button onClick={resetFilters} variant="outlined" color="secondary">
              Limpiar
            </Button>
            <Button onClick={applyFilters} variant="contained" color="primary" startIcon={<Search />}>
              Aplicar Filtros
            </Button>
          </DialogActions>
        </Dialog>

        {/* Tabla de inventario */}
        <table className="styled-table">
          <thead>
            <tr>
              <th>ID Producto</th>
              <th>Nombre Producto</th>
              <th>Descripción</th>
              <th>Código de Barras</th>
              <th>Precio ARS</th>
              <th>Precio USD</th>
              <th>Stock Actual</th>
              <th>Almacén</th>
              <th>Estante</th>
              <th>Fecha Alta</th>
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
                  <td>{producto.precio_costo_ars}</td>
                  <td>{producto.precio_costo_usd}</td>
                  <td>{producto.stock_actual}</td>
                  <td>{producto.almacen_descripcion}</td>
                  <td>{producto.descripcion_estante}</td>
                  <td>{new Date(producto.fecha_ingreso).toLocaleString()}</td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="8">No hay productos en inventario.</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </>
  );
};

export default Inventario;
