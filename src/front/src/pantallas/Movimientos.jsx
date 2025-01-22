import React, { useState, useEffect } from "react";
import $ from "jquery";
import "datatables.net";
import "datatables.net-dt/css/jquery.datatables.min.css";
import axios from "axios";

const MovimientosStock = () => {
  const [movimientos, setMovimientos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [tipoMovimiento, setTipoMovimiento] = useState("");
  const [fechaDesde, setFechaDesde] = useState("");
  const [fechaHasta, setFechaHasta] = useState("");
  const [table, setTable] = useState(null);

  // Obtener movimientos de stock desde el backend
  useEffect(() => {
    const obtenerMovimientos = async () => {
      try {
        const response = await axios.post(
          `${import.meta.env.VITE_API_BASE_URL}/tabla_consulta_stock_movimientos`,
          {}
        );
        setMovimientos(response.data || []);
      } catch (error) {
        console.error("Error al obtener los movimientos del stock:", error);
      } finally {
        setLoading(false);
      }
    };

    obtenerMovimientos();
  }, []);

  // Inicializar DataTable cuando los datos son cargados
  useEffect(() => {
    if (movimientos.length > 0) {
      // Destruir tabla si ya existe para evitar duplicados
      if ($.fn.DataTable.isDataTable("#tablaMovimientos")) {
        $("#tablaMovimientos").DataTable().destroy();
      }

      // Inicializar DataTable
      const newTable = $("#tablaMovimientos").DataTable({
        responsive: true,
        language: {
          url: "//cdn.datatables.net/plug-ins/1.13.6/i18n/es-ES.json",
        },
        dom: "Bfrtip", // Botones, filtro, tabla
        buttons: ["copy", "excel", "pdf"], // Exportar opciones
        ordering: true, // Habilitar ordenamiento
      });

      // Establecer la tabla en el estado
      setTable(newTable);
    }
  }, [movimientos]);

  // Filtro de fecha y tipo de movimiento
  const aplicarFiltros = () => {
    if (table) {
      // Filtro por tipo de movimiento
      table.column(7).search(tipoMovimiento).draw();

      // Filtro por rango de fechas
      $.fn.dataTable.ext.search.push((settings, data, dataIndex) => {
        const fechaMovimiento = new Date(data[3]); // Columna de la fecha de movimiento
        const desde = new Date(fechaDesde);
        const hasta = new Date(fechaHasta);

        // Si la fecha es válida y se encuentra en el rango, devolver true
        if (
          (isNaN(desde) || fechaMovimiento >= desde) &&
          (isNaN(hasta) || fechaMovimiento <= hasta)
        ) {
          return true;
        }
        return false;
      });

      // Aplicar el filtrado
      table.draw();
    }
  };

  // Si los datos aún están cargando, mostrar un mensaje de carga
  if (loading) {
    return <div>Cargando...</div>;
  }

  return (
    <div>
      <h2>Movimientos de Stock</h2>

      {/* Filtros */}
      <div style={{ marginBottom: "20px" }}>
        <label>Tipo de Movimiento:</label>
        <select
          onChange={(e) => setTipoMovimiento(e.target.value)}
          value={tipoMovimiento}
          style={{ marginRight: "10px" }}
        >
          <option value="">Todos</option>
          <option value="1">Entrada</option>
          <option value="2">Salida</option>
          {/* Agregar más opciones según los tipos de movimiento */}
        </select>

        <label>Fecha Desde:</label>
        <input
          type="date"
          onChange={(e) => setFechaDesde(e.target.value)}
          style={{ marginRight: "10px" }}
        />

        <label>Fecha Hasta:</label>
        <input
          type="date"
          onChange={(e) => setFechaHasta(e.target.value)}
          style={{ marginRight: "10px" }}
        />

        {/* Botón para aplicar los filtros */}
        <button onClick={aplicarFiltros}>Filtrar</button>
      </div>

      {/* Tabla */}
      <div style={{ overflowX: "auto" }}>
        <table id="tablaMovimientos" className="display">
          <thead>
            <tr>
              <th>ID Movimiento</th>
              <th>ID Stock</th>
              <th>Cantidad</th>
              <th>Fecha Movimiento</th>
              <th>ID Usuario</th>
              <th>ID Proveedor</th>
              <th>Descripción</th>
              <th>Tipo Movimiento</th>
            </tr>
          </thead>
          <tbody>
            {movimientos.map((movimiento) => (
              <tr key={movimiento.id_stock_movimiento}>
                <td>{movimiento.id_stock_movimiento}</td>
                <td>{movimiento.id_stock}</td>
                <td>{movimiento.cantidad}</td>
                <td>{new Date(movimiento.fecha_movimiento).toLocaleString()}</td>
                <td>{movimiento.id_usuario}</td>
                <td>{movimiento.id_proveedor}</td>
                <td>{movimiento.descripcion}</td>
                <td>{movimiento.id_tipo_movimiento}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default MovimientosStock;
