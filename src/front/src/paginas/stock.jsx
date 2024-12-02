import React, { useState } from 'react';
import '../styles/stock.css';
import AgregarProducto from '../components/AgregarProducto'; // Asegúrate que el import esté correcto
import TablaProductos from '../components/TablaProductos';

const Stock = () => {
    const [productos, setProductos] = useState([]);

    // Función que maneja cuando se agrega un producto
    const manejarProductoAgregado = (nuevoProducto) => {
        setProductos([...productos, nuevoProducto]); // Agregar el producto a la lista
    };

    return (
        <div className="content">
            <div className="half">
                {/* Asegúrate de pasar correctamente la función onProductoAgregado */}
                <AgregarProducto onProductoAgregado={manejarProductoAgregado} />
            </div>
            <div className="half">
                <TablaProductos productos={productos} />
            </div>
        </div>
    );
};

export default Stock;
