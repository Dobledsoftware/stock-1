import React, { useState } from "react";

const Ventas = () => {
  // Estado para el término de búsqueda
  const [busqueda, setBusqueda] = useState("");
  
  // Estado para almacenar el carrito
  const [carrito, setCarrito] = useState([]);
  
  // Estado para el método de pago
  const [metodoPago, setMetodoPago] = useState("");
  
  // Estado para la cantidad de dinero entregado (solo en efectivo)
  const [dineroEntregado, setDineroEntregado] = useState(0);

  // Datos de ejemplo de ventas
  const ventas = [
    { id: 7790520028785, producto: "Producto A", cantidad: 2, precio: 10.0, total: 20.0 },
    { id: 2, producto: "Producto B", cantidad: 1, precio: 15.5, total: 15.5 },
    { id: 3, producto: "Producto C", cantidad: 5, precio: 5.0, total: 25.0 },
    { id: 4, producto: "Producto D", cantidad: 3, precio: 12.0, total: 36.0 },
  ];

  // Filtrar ventas según el término de búsqueda por ID
  const ventasFiltradas = ventas.filter(venta =>
    venta.id.toString().includes(busqueda)
  );

  // Función para agregar productos al carrito
  const agregarAlCarrito = (producto) => {
    setCarrito([...carrito, producto]);
  };

  // Función para calcular el total del carrito
  const calcularTotalCarrito = () => {
    return carrito.reduce((total, producto) => total + producto.total, 0).toFixed(2);
  };

  // Función para calcular el cambio si el pago es en efectivo
  const calcularCambio = () => {
    const total = parseFloat(calcularTotalCarrito());
    if (metodoPago === "efectivo" && dineroEntregado >= total) {
      return (dineroEntregado - total).toFixed(2);
    }
    return "0.00"; // Si no es efectivo o no hay suficiente dinero, no mostrar cambio
  };

  return (
    <div style={{ padding: "20px" }}>
     {/* <h1>Gestión de Ventas</h1>
       <p>Desde aquí puedes gestionar las ventas realizadas.</p>
      <button onClick={() => alert("Agregar venta")}>Agregar Venta</button>
 */}
      {/* Buscador por ID */}
      <input
        type="text"
        placeholder="Buscar por ID..."
        value={busqueda}
        onChange={(e) => setBusqueda(e.target.value)}
        style={{
          padding: "10px",
          fontSize: "1rem",
          width: "100%",
          marginTop: "20px",
          marginBottom: "20px",
          border: "1px solid #ccc",
          borderRadius: "5px",
        }}
      />

      {/* Tabla de ventas filtradas */}
      <table style={{ marginTop: "20px", width: "100%", borderCollapse: "collapse" }}>
        <thead>
          <tr>
            <th style={{ border: "1px solid #ddd", padding: "8px" }}>ID</th>
            <th style={{ border: "1px solid #ddd", padding: "8px" }}>Producto</th>
            <th style={{ border: "1px solid #ddd", padding: "8px" }}>Cantidad</th>
            <th style={{ border: "1px solid #ddd", padding: "8px" }}>Precio</th>
            <th style={{ border: "1px solid #ddd", padding: "8px" }}>Total</th>
            <th style={{ border: "1px solid #ddd", padding: "8px" }}>Acciones</th>
          </tr>
        </thead>
        <tbody>
          {ventasFiltradas.length > 0 ? (
            ventasFiltradas.map((venta) => (
              <tr key={venta.id}>
                <td style={{ border: "1px solid #ddd", padding: "8px" }}>{venta.id}</td>
                <td style={{ border: "1px solid #ddd", padding: "8px" }}>{venta.producto}</td>
                <td style={{ border: "1px solid #ddd", padding: "8px" }}>{venta.cantidad}</td>
                <td style={{ border: "1px solid #ddd", padding: "8px" }}>${venta.precio.toFixed(2)}</td>
                <td style={{ border: "1px solid #ddd", padding: "8px" }}>${venta.total.toFixed(2)}</td>
                <td style={{ border: "1px solid #ddd", padding: "8px" }}>
                  <button onClick={() => alert("Editar venta")}>Editar</button>
                  <button
                    onClick={() => alert("Eliminar venta")}
                    style={{ marginLeft: "10px" }}
                  >
                    Eliminar
                  </button>
                  {/* Botón para agregar al carrito */}
                  <button
                    onClick={() => agregarAlCarrito(venta)}
                    style={{ marginLeft: "10px", backgroundColor: "#4CAF50", color: "white", padding: "5px 10px", borderRadius: "4px" }}
                  >
                    Agregar al Carrito
                  </button>
                </td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="6" style={{ textAlign: "center", padding: "10px" }}>
                No se encontraron ventas.
              </td>
            </tr>
          )}
        </tbody>
      </table>

      {/* Carrito */}
      <div style={{ marginTop: "30px", borderTop: "2px solid #ccc", paddingTop: "20px" }}>
        <h2>Carrito de Compras</h2>
        {carrito.length > 0 ? (
          <>
            <table style={{ width: "100%", borderCollapse: "collapse" }}>
              <thead>
                <tr>
                  <th style={{ border: "1px solid #ddd", padding: "8px" }}>ID</th>
                  <th style={{ border: "1px solid #ddd", padding: "8px" }}>Producto</th>
                  <th style={{ border: "1px solid #ddd", padding: "8px" }}>Cantidad</th>
                  <th style={{ border: "1px solid #ddd", padding: "8px" }}>Precio</th>
                  <th style={{ border: "1px solid #ddd", padding: "8px" }}>Total</th>
                </tr>
              </thead>
              <tbody>
                {carrito.map((producto, index) => (
                  <tr key={index}>
                    <td style={{ border: "1px solid #ddd", padding: "8px" }}>{producto.id}</td>
                    <td style={{ border: "1px solid #ddd", padding: "8px" }}>{producto.producto}</td>
                    <td style={{ border: "1px solid #ddd", padding: "8px" }}>{producto.cantidad}</td>
                    <td style={{ border: "1px solid #ddd", padding: "8px" }}>${producto.precio.toFixed(2)}</td>
                    <td style={{ border: "1px solid #ddd", padding: "8px" }}>${producto.total.toFixed(2)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
            <div style={{ marginTop: "20px" }}>
              <strong>Total: </strong>${calcularTotalCarrito()}
            </div>
          </>
        ) : (
          <p>No hay productos en el carrito.</p>
        )}

        {/* Método de pago */}
        <div style={{ marginTop: "20px" }}>
          <label htmlFor="metodoPago" style={{ marginRight: "10px" }}>
            Método de pago:
          </label>
          <select
            id="metodoPago"
            value={metodoPago}
            onChange={(e) => setMetodoPago(e.target.value)}
            style={{
              padding: "10px",
              fontSize: "1rem",
              border: "1px solid #ccc",
              borderRadius: "5px",
            }}
          >
            <option value="">Seleccionar método</option>
            <option value="tarjeta">Tarjeta de Crédito</option>
            <option value="paypal">PayPal</option>
            <option value="efectivo">Efectivo</option>
          </select>
        </div>

        {/* Solo mostrar campo para dinero entregado si el método de pago es en efectivo */}
        {metodoPago === "efectivo" && (
          <div style={{ marginTop: "20px" }}>
            <label htmlFor="dineroEntregado" style={{ marginRight: "10px" }}>
              Dinero entregado:
            </label>
            <input
              type="number"
              id="dineroEntregado"
              value={dineroEntregado}
              onChange={(e) => setDineroEntregado(parseFloat(e.target.value))}
              style={{
                padding: "10px",
                fontSize: "1rem",
                border: "1px solid #ccc",
                borderRadius: "5px",
                width: "100px",
              }}
            />
          </div>
        )}

        {/* Mostrar cambio si es efectivo */}
        {metodoPago === "efectivo" && dineroEntregado >= parseFloat(calcularTotalCarrito()) && (
          <div style={{ marginTop: "20px" }}>
            <strong>Cambio: </strong>${calcularCambio()}
          </div>
        )}
      </div>
    </div>
  );
};

export default Ventas;
