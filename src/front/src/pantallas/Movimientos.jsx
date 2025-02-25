import React, { useState, useEffect } from "react";
import $ from "jquery";
import "datatables.net";
import "datatables.net-dt/css/jquery.datatables.min.css";
import axios from "axios";

const MovimientosStock = () => {
  const [eventos, setEventos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [idProducto, setIdProducto] = useState("");
  const [idUsuario, setIdUsuario] = useState("");
  const [fechaInicio, setFechaInicio] = useState("");
  const [fechaFin, setFechaFin] = useState("");
  const [idTipoMovimiento, setIdTipoMovimiento] = useState("");
  const [tiposMovimiento, setTiposMovimiento] = useState([]);
  const [modalOpen, setModalOpen] = useState(false);
  const [table, setTable] = useState(null);

  const obtenerTiposMovimiento = async () => {
    try {
      const response = await axios.get(
        `${import.meta.env.VITE_API_BASE_URL}/tipo_movimiento_stock`,
        { params: { estado: true } }
      );
      if (response.data && Array.isArray(response.data.data)) {
        setTiposMovimiento(response.data.data);
      } else {
        setTiposMovimiento([]);
      }
    } catch (error) {
      console.error("Error al obtener los tipos de movimiento:", error);
      setTiposMovimiento([]);
    }
  };

  const obtenerMovimientos = async () => {
    try {
      setLoading(true);
      const response = await axios.get(
        `${import.meta.env.VITE_API_BASE_URL}/tabla_consulta_stock_movimientos`,
        {
          params: {
            id_producto: idProducto || undefined,
            id_usuario: idUsuario || undefined,
            fecha_inicio: fechaInicio || undefined,
            fecha_fin: fechaFin || undefined,
            id_tipo_movimiento: idTipoMovimiento || undefined,
          },
        }
      );
      setEventos(response.data || []);
    } catch (error) {
      console.error("Error al obtener los movimientos del stock:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    obtenerTiposMovimiento();
    obtenerMovimientos();
  }, []);

  return (
    <div>
      <h2>Eventos de Movimientos de Stock</h2>
      <button onClick={() => setModalOpen(true)}>Filtrar</button>

      {modalOpen && (
        <div className="modal">
          <div className="modal-content">
            <h3>Filtrar Movimientos</h3>
            <label>ID Producto:</label>
            <input type="number" onChange={(e) => setIdProducto(e.target.value)} value={idProducto} />
            <label>ID Usuario:</label>
            <input type="number" onChange={(e) => setIdUsuario(e.target.value)} value={idUsuario} />
            <label>Tipo de Movimiento:</label>
            <select onChange={(e) => setIdTipoMovimiento(e.target.value)} value={idTipoMovimiento}>
              <option value="">Todos</option>
              {tiposMovimiento.length > 0 && tiposMovimiento.map((tipo) => (
                <option key={tipo.id_tipo_movimiento} value={tipo.id_tipo_movimiento}>{tipo.descripcion}</option>
              ))}
            </select>
            <label>Fecha Inicio:</label>
            <input type="date" onChange={(e) => setFechaInicio(e.target.value)} value={fechaInicio} />
            <label>Fecha Fin:</label>
            <input type="date" onChange={(e) => setFechaFin(e.target.value)} value={fechaFin} />
            <button onClick={() => { obtenerMovimientos(); setModalOpen(false); }}>Aplicar Filtros</button>
            <button onClick={() => setModalOpen(false)}>Cerrar</button>
          </div>
        </div>
      )}

      <div style={{ overflowX: "auto" }}>
        <table id="tablaEventos" className="display compact" style={{ fontSize: "12px" }}>
          <thead>
            <tr>
              <th style={{ width: "80px" }}>ID Evento</th>
              <th>Movimientos</th>
            </tr>
          </thead>
          <tbody>
            {eventos.map((evento) => (
              <tr key={evento.identificador_evento}>
                <td>{evento.identificador_evento}</td>
                <td>
                  <table className="display compact" style={{ fontSize: "12px" }}>
                    <thead>
                      <tr>
                        <th>ID Movimiento</th>
                        <th>Cantidad</th>
                        <th>Descripción</th>
                        <th>Fecha Movimiento</th>
                        <th>Tipo Movimiento</th>
                        <th>Nombre Producto</th>
                        <th>Descripción Producto</th>
                        <th>Marca Producto</th>
                      </tr>
                    </thead>
                    <tbody>
                      {evento.movimientos.map((movimiento) => (
                        <tr key={movimiento.id_stock_movimiento}>
                          <td>{movimiento.id_stock_movimiento}</td>
                          <td>{movimiento.cantidad}</td>
                          <td>{movimiento.descripcion}</td>
                          <td>{new Date(movimiento.fecha_movimiento).toLocaleString()}</td>
                          <td>{movimiento.tipo_movimiento}</td>
                          <td>{movimiento.nombre_producto}</td>
                          <td>{movimiento.descripcion_producto}</td>
                          <td>{movimiento.marca_producto}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default MovimientosStock;
