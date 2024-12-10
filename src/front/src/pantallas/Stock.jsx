import React, { useState } from "react";
import AgregarProducto from '../components/AgregarProducto'; // Importar el componente del modal
import TablaProductos from '../components/TablaProductos'; // Importar la tabla de productos

const Stock = () => {
  const [productos, setProductos] = useState([]); // Estado para la lista de productos
  const [modalVisible, setModalVisible] = useState(false); // Estado para controlar la visibilidad del modal

  // Función que maneja la adición de un producto
  const manejarProductoAgregado = (nuevoProducto) => {
    setProductos([...productos, nuevoProducto]); // Agregar el nuevo producto
    setModalVisible(false); // Cerrar el modal después de agregar
  };

  // Función para abrir el modal
  const manejarAbrirModal = () => {
    setModalVisible(true);
  };

  // Función para cerrar el modal
  const manejarCerrarModal = () => {
    setModalVisible(false);
  };

  return (
    <div className="content">
      <div className="half">
        {/* Botón para abrir el modal */}
        <button onClick={manejarAbrirModal}>Agregar Producto</button>

        {/* Mostrar el modal solo si modalVisible es true */}
        {modalVisible && (
          <AgregarProducto
            onClose={manejarCerrarModal} // Pasar la función para cerrar el modal
            onProductoAgregado={manejarProductoAgregado} // Pasar la función para agregar un producto
          />
        )}
      </div>
      <div className="half">
        {/* Tabla de productos */}
        <TablaProductos productos={productos} />
      </div>
    </div>
  );
};

export default Stock;
