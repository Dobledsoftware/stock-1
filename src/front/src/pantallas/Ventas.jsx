import React, { useState, useEffect } from "react";
import axios from "axios";

export default function PanelVentas() {
  const [productos, setProductos] = useState([]);
  const [busqueda, setBusqueda] = useState("");
  const [carrito, setCarrito] = useState([]);

  // Cargar los productos desde el servidor al montar el componente
  useEffect(() => {
    const obtenerProductos = async () => {
      try {
        const response = await axios.post(
          `${import.meta.env.VITE_API_BASE_URL}/producto`,
          {
            accion: "verTodosLosProductos",
            estado: "Activo",
          }
        );

        if (response.data && Array.isArray(response.data.data)) {
          setProductos(response.data.data);
        } else {
          console.error("Respuesta inesperada:", response.data);
        }
      } catch (error) {
        console.error("Error al cargar productos:", error);
      }
    };

    obtenerProductos();
  }, []);

  // Filtrar productos según la búsqueda
  const productosFiltrados = productos.filter((producto) => {
    const valores = [
      producto.producto_id?.toString(),
      producto.producto_nombre?.toLowerCase(),
      producto.producto_marca?.toLowerCase(),
      producto.producto_codigo_barras?.toLowerCase(),
    ];
    return valores.some((valor) =>
      valor?.includes(busqueda.toLowerCase())
    );
  });

  // Agregar producto al carrito
  const agregarAlCarrito = (producto) => {
    setCarrito((prevCarrito) => [...prevCarrito, producto]);
  };

  // Quitar producto del carrito
  const quitarDelCarrito = (id) => {
    setCarrito((prevCarrito) =>
      prevCarrito.filter((item) => item.producto_id !== id)
    );
  };

  // Calcular el total de la venta
  const calcularTotal = () => {
    return carrito.reduce((total, producto) => total + producto.producto_precio, 0);
  };

  // Realizar la venta
  const realizarVenta = () => {
    console.log("Venta realizada con los productos:", carrito);
    // Aquí se enviaría el carrito al backend para registrar la venta
    setCarrito([]); // Limpiar el carrito después de la venta
  };

  return (
    <div>
      <h1>Panel de Ventas</h1>
      <div>
        <input
          type="text"
          placeholder="Buscar producto"
          value={busqueda}
          onChange={(e) => setBusqueda(e.target.value)}
        />
      </div>
      <h2>Productos</h2>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Nombre</th>
            <th>Marca</th>
            <th>Precio venta ARS</th>
            <th>Precio venta USD</th>
            <th>Código de Barras</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          {productosFiltrados.map((producto) => (
            <tr key={producto.producto_id}>
              <td>{producto.producto_id}</td>
              <td>{producto.producto_nombre}</td>
              <td>{producto.producto_marca}</td>
              <td>${producto.precio_venta_ars}</td>
              <td>${producto.precio_venta_usd}</td>
              <td>{producto.producto_codigo_barras}</td>
              <td>
                <button onClick={() => agregarAlCarrito(producto)}>
                  Agregar
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      <h2>Carrito</h2>
      {carrito.length > 0 ? (
        <div>
          <table>
            <thead>
              <tr>
                <th>Nombre</th>
                <th>Marca</th>
                <th>Precio Venta ARS</th>
                <th>Precio Venta USD</th>

                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              {carrito.map((producto) => (
                <tr key={producto.producto_id}>
                  <td>{producto.producto_nombre}</td>
                  <td>{producto.producto_marca}</td>
                  <td>${producto.precio_venta_ars}</td>
                  <td>${producto.precio_venta_usd}</td>
                  <td>
                    <button onClick={() => quitarDelCarrito(producto.producto_id)}>
                      Quitar
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          <h3>Total: ${calcularTotal()}</h3>
          <button onClick={realizarVenta}>Realizar Venta</button>
        </div>
      ) : (
        <p>El carrito está vacío</p>
      )}
    </div>
  );
}


