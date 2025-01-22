import React, { useState } from "react";
import AgregarProducto from "../components/AgregarProducto"; // Modal para agregar productos
import TablaProductos from "../components/TablaProductos"; // Tabla de productos
import Categorias from "../components/Categorias"; // Modal para gestionar categorías
/* import '../styles/stock.css'; */

const Productos = ({ apiBaseUrl }) => {
  const [productos, setProductos] = useState([]); // Estado para la lista de productos
  const [modalProductoVisible, setModalProductoVisible] = useState(false); // Control del modal de productos
  const [modalCategoriasVisible, setModalCategoriasVisible] = useState(false); // Control del modal de categorías

  // Función para agregar un producto y cerrar el modal
  const manejarProductoAgregado = (nuevoProducto) => {
    setProductos([...productos, nuevoProducto]); // Agregar el producto al estado
    setModalProductoVisible(false); // Cerrar el modal
  };

  // Función para abrir el modal de productos
  const manejarAbrirModalProducto = () => {
    setModalProductoVisible(true);
  };

  // Función para cerrar el modal de productos
  const manejarCerrarModalProducto = () => {
    setModalProductoVisible(false);
  };



  return (
    <div className="content">
      <div className="half">
        {/* Botón para abrir el modal de productos */}
        <button onClick={manejarAbrirModalProducto}>Agregar Producto</button>

        {/* Modal de productos */}
        {modalProductoVisible && (
          <div className="modal">
            <div className="modal-content">
              <span className="close" onClick={manejarCerrarModalProducto}>
                &times;
              </span>
              <AgregarProducto
                onClose={manejarCerrarModalProducto}
                onProductoAgregado={manejarProductoAgregado}
              />
            </div>
          </div>
        )}

        
      </div>

      <div className="half">
        {/* Tabla de productos */}
        <TablaProductos productos={productos} />
      </div>
    </div>
  );
};

export default Productos;
