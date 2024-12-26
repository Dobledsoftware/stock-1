import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import '../styles/AgregarProducto.module.css';
import { toast } from 'react-toastify'; // Importamos toast
import Swal from 'sweetalert2';  // Importamos SweetAlert2

const AgregarProducto = ({ onProductoAgregado, onClose }) => {
    const [formData, setFormData] = useState({
        nombre: '',
        descripcion: '',
        precio: '',
        id_marca: '',
        id_categoria: '',
        codigo_barras: '',
    });
    const [categorias, setCategorias] = useState([]);
    const [marcas, setMarcas] = useState([]);

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData((prev) => ({ ...prev, [name]: value }));
    };

    const fetchData = async (url, setState, body) => {
        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(body),
            });

            if (response.ok) {
                const { data } = await response.json();
                setState(data);
            } else {
                throw new Error('Error al obtener datos del servidor.');
            }
        } catch (err) {
            toast.error(`Error: ${err.message}`);  // Usamos Toastify para mostrar error
        }
    };

    useEffect(() => {
        fetchData(
            `${import.meta.env.VITE_API_BASE_URL}/producto_categoria`,
            setCategorias,
            { accion: 'verTodasLasCategorias', incluir_inactivas: true }
        );
        fetchData(
            `${import.meta.env.VITE_API_BASE_URL}/producto_marca`,
            setMarcas,
            { accion: 'verTodasLasMarcas', incluir_inactivas: true }
        );
    }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();

        const producto = {
            accion: 'agregarProducto',
            nombre: formData.nombre,
            descripcion: formData.descripcion,
            precio: parseFloat(formData.precio),
            codigo_barras: formData.codigo_barras,
            id_marca: formData.id_marca ? parseInt(formData.id_marca, 10) : null,
            id_categoria: formData.id_categoria ? parseInt(formData.id_categoria, 10) : null,
            forceAdd: false,
        };

        try {
            const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/producto`, {
                method: 'POST',
                body: JSON.stringify(producto),
                headers: { 'Content-Type': 'application/json' },
            });

            if (response.ok) {
                const { status, message, productos_repetidos } = await response.json();
                
                // Si el status es warning, mostramos una alerta con los productos repetidos
                if (status === 'warning' && productos_repetidos.length > 0) {
                    const productos = productos_repetidos.map(
                        (prod) => `- ${prod.nombre} (Código: ${prod.codigo_barras})`
                    ).join('\n');

                    Swal.fire({
                        title: '¡Advertencia!',
                        text: `Ya existen productos con el código de barras:\n${productos}\n¿Desea agregar el producto de todos modos?`,
                        icon: 'warning',
                        showCancelButton: true,
                        confirmButtonText: 'Sí, agregar',
                        cancelButtonText: 'No, cancelar',
                    }).then((result) => {
                        if (result.isConfirmed) {
                            producto.forceAdd = true;
                            agregarProductoConConfirmacion(producto);
                        }
                    });
                } else {
                    // Si la respuesta es exitosa y no hay productos repetidos
                    Swal.fire({
                        title: '¡Éxito!',
                        text: message,
                        icon: 'success',
                        confirmButtonText: 'Aceptar',
                    });

                    onProductoAgregado(); // Llamamos la función para actualizar la lista de productos
                    onClose(); // Cerramos el modal
                    resetForm();
                }
            } else {
                const { message } = await response.json();
                toast.error(`Error: ${message || 'Error al agregar el producto'}`);
            }
        } catch (err) {
            toast.error(`Error: ${err.message}`);
        }
    };

    const agregarProductoConConfirmacion = async (producto) => {
        try {
            const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/producto`, {
                method: 'POST',
                body: JSON.stringify(producto),
                headers: { 'Content-Type': 'application/json' },
            });

            if (response.ok) {
                const { message } = await response.json();
                Swal.fire({
                    title: '¡Éxito!',
                    text: message,
                    icon: 'success',
                    confirmButtonText: 'Aceptar',
                });

                onProductoAgregado();
                onClose();
                resetForm();
            } else {
                const { message } = await response.json();
                toast.error(`Error: ${message || 'Error al agregar el producto'}`);
            }
        } catch (err) {
            toast.error(`Error: ${err.message}`);
        }
    };

    const resetForm = () => {
        setFormData({
            nombre: '',
            descripcion: '',
            precio: '',
            id_marca: '',
            id_categoria: '',
            codigo_barras: '',
        });
    };

    return (
        <div className="modal">
            <div className="modal-content">
                <span className="close" onClick={onClose}>&times;</span>
                <h2>Agregar Producto</h2>
                <form onSubmit={handleSubmit}>
                    <input
                        type="text"
                        name="nombre"
                        placeholder="Nombre"
                        value={formData.nombre}
                        onChange={handleInputChange}
                        required
                    />
                    <input
                        type="text"
                        name="descripcion"
                        placeholder="Descripción"
                        value={formData.descripcion}
                        onChange={handleInputChange}
                        required
                    />
                    <input
                        type="number"
                        name="precio"
                        placeholder="Precio"
                        value={formData.precio}
                        onChange={handleInputChange}
                        required
                    />
                    <select
                        name="id_categoria"
                        value={formData.id_categoria}
                        onChange={handleInputChange}
                        required
                    >
                        <option value="" disabled>Seleccionar categoría</option>
                        {categorias.map((categoria) => (
                            <option key={categoria.id_categoria} value={categoria.id_categoria}>
                                {categoria.descripcion}
                            </option>
                        ))}
                    </select>
                    <select
                        name="id_marca"
                        value={formData.id_marca}
                        onChange={handleInputChange}
                        required
                    >
                        <option value="" disabled>Seleccionar marca</option>
                        {marcas.map((marca) => (
                            <option key={marca.id_marca} value={marca.id_marca}>
                                {marca.descripcion}
                            </option>
                        ))}
                    </select>
                    <input
                        type="text"
                        name="codigo_barras"
                        placeholder="Código de Barras"
                        value={formData.codigo_barras}
                        onChange={handleInputChange}
                        required
                    />
                    <button type="submit">Agregar Producto</button>
                </form>
            </div>
        </div>
    );
};

AgregarProducto.propTypes = {
    onProductoAgregado: PropTypes.func.isRequired,
    onClose: PropTypes.func.isRequired,
};

export default AgregarProducto;
