import React, { useState } from 'react';
import PropTypes from 'prop-types';
import '../styles/AgregarProducto.css';  // Asegúrate de incluir los estilos necesarios

const AgregarProducto = ({ onProductoAgregado, onClose }) => {
    const [nombre, setNombre] = useState('');
    const [descripcion, setDescripcion] = useState('');
    const [precio, setPrecio] = useState('');
    const [stock, setStock] = useState('');
    const [proveedorId, setProveedorId] = useState('');
    const [imagen, setImagen] = useState(null); // Para almacenar la imagen seleccionada
    const [mensaje, setMensaje] = useState('');
    const [error, setError] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();

        const nuevoProducto = {
            accion: 'agregarProducto',
            nombre,
            descripcion,
            precio: parseFloat(precio),
            stock_actual: parseInt(stock),
            id_proveedor: parseInt(proveedorId),
            imagen, // Incluir la imagen en los datos
        };

        try {
            const formData = new FormData();
            formData.append('producto', JSON.stringify(nuevoProducto));
            if (imagen) {
                formData.append('imagen', imagen); // Agregar la imagen
            }

            const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/producto`, {
                method: 'POST',
                body: formData,
            });

            if (response.ok) {
                const data = await response.json();
                setMensaje('Producto agregado exitosamente');
                setError('');
                onProductoAgregado(data);
                onClose(); // Cerrar el modal al agregar el producto
                setNombre('');
                setDescripcion('');
                setPrecio('');
                setStock('');
                setProveedorId('');
                setImagen(null);
            } else {
                const errorData = await response.json();
                throw new Error(errorData.message || 'Error al agregar el producto');
            }
        } catch (error) {
            setError(`Error: ${error.message}`);
            setMensaje('');
        }
    };

    const handleImageChange = (e) => {
        const file = e.target.files[0];
        if (file) {
            setImagen(file);
        }
    };

    return (
        <div className="modal">
            <div className="modal-content">
                <span className="close" onClick={onClose}>&times;</span>
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
                    <div className="file-input-container">
                        <input
                            type="file"
                            onChange={handleImageChange}
                            accept="image/*"
                        />
                        {imagen && <p>Imagen seleccionada: {imagen.name}</p>}
                    </div>
                    <button type="submit">Agregar Producto</button>
                </form>

                {mensaje && <p className="mensaje-exito">{mensaje}</p>}
                {error && <p className="mensaje-error">{error}</p>}
            </div>
        </div>
    );
};

AgregarProducto.propTypes = {
    onProductoAgregado: PropTypes.func.isRequired,
    onClose: PropTypes.func.isRequired,
};

export default AgregarProducto;
