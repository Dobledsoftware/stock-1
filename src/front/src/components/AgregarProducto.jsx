import React, { useState } from 'react';
import PropTypes from 'prop-types';
import '../styles/AgregarProducto.css';

const AgregarProducto = ({ onProductoAgregado }) => {
    const [nombre, setNombre] = useState('');
    const [descripcion, setDescripcion] = useState('');
    const [precio, setPrecio] = useState('');
    const [stock, setStock] = useState('');
    const [proveedorId, setProveedorId] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();

        // Crear el objeto del nuevo producto
        const nuevoProducto = {
            producto_nombre: nombre,
            producto_descripcion: descripcion,
            producto_precio: precio,
            producto_stock: stock,
            proveedor_id: proveedorId,
        };

        // Llamar a la función onProductoAgregado para pasar el nuevo producto
        onProductoAgregado(nuevoProducto);
    };

    return (
        <div>
            <h2>Agregar Producto</h2>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    placeholder="Nombre"
                    value={nombre}
                    onChange={(e) => setNombre(e.target.value)}
                    required
                />
                <input
                    type="text"
                    placeholder="Descripción"
                    value={descripcion}
                    onChange={(e) => setDescripcion(e.target.value)}
                    required
                />
                <input
                    type="number"
                    placeholder="Precio"
                    value={precio}
                    onChange={(e) => setPrecio(e.target.value)}
                    required
                />
                <input
                    type="number"
                    placeholder="Stock"
                    value={stock}
                    onChange={(e) => setStock(e.target.value)}
                    required
                />
                <input
                    type="number"
                    placeholder="Proveedor ID"
                    value={proveedorId}
                    onChange={(e) => setProveedorId(e.target.value)}
                    required
                />
                <button type="submit">Agregar Producto</button>
            </form>
        </div>
    );
};

AgregarProducto.propTypes = {
    onProductoAgregado: PropTypes.func.isRequired, // Prop requerida de tipo función
};

export default AgregarProducto;
