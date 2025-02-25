import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import '../styles/AgregarProducto.module.css';
import { toast } from 'react-toastify'; // Importamos toast
import Swal from 'sweetalert2'; // Importamos SweetAlert2

const AgregarProducto = ({ onProductoAgregado, onClose }) => {
    const [formData, setFormData] = useState({
        nombre: '',
        descripcion: '',
        precio_venta_ars: '',
        precio_venta_usd: '',
        id_marca: '',
        id_categoria: '',
        codigo_barras: '',
        estado: 'Activo', // El estado puede ser 'Activo' o 'Inactivo'
    });
    const [categorias, setCategorias] = useState([]);
    const [marcas, setMarcas] = useState([]);

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData((prev) => ({ ...prev, [name]: value }));
    };

    // Función para realizar las peticiones fetch
    const fetchData = async (url, setState, params = {}) => {
        try {
            const response = await fetch(url, {
                method: 'GET', // Cambiado a GET ya que se usa un endpoint GET para categorías y marcas
                headers: { 'Content-Type': 'application/json' },
                params: params,
            });

            if (!response.ok) {
                throw new Error('Error al obtener datos del servidor');
            }

            const { data } = await response.json();
            setState(data);
        } catch (err) {
            toast.error(`Error: ${err.message}`);
        }
    };

    useEffect(() => {
        const baseUrl = import.meta.env.VITE_API_BASE_URL;

        // Realizar las peticiones de categorías y marcas
        fetchData(`${baseUrl}/productos_categorias?estado=true`, setCategorias);
        fetchData(`${baseUrl}/producto_marcas?estado=true`, setMarcas);
    }, []);

    // Enviar los datos al servidor para agregar el producto
    const handleSubmit = async (e) => {
        e.preventDefault();

        const producto = {
            accion: 'agregarProducto',
            nombre: formData.nombre,
            descripcion: formData.descripcion,
            precio_venta_ars: parseFloat(formData.precio_venta_ars),
            precio_venta_usd: parseFloat(formData.precio_venta_usd),
            codigo_barras: formData.codigo_barras,
            id_marca: formData.id_marca ? parseInt(formData.id_marca, 10) : null,
            id_categoria: formData.id_categoria ? parseInt(formData.id_categoria, 10) : null,
            estado: formData.estado === 'Activo', // Transformamos a booleano
            forceAdd: false,
        };

        try {
            const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/producto`, {
                method: 'POST',
                body: JSON.stringify(producto),
                headers: { 'Content-Type': 'application/json' },
            });

            const { status, message, productos_repetidos } = await response.json();

            if (status === 'warning' && productos_repetidos.length > 0) {
                // Mostrar una alerta si hay productos repetidos
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
                // Si no hay productos repetidos, mostrar el mensaje de éxito
                Swal.fire({
                    title: '¡Éxito!',
                    text: message,
                    icon: 'success',
                    confirmButtonText: 'Aceptar',
                });

                onProductoAgregado(); // Actualizar lista de productos
                onClose(); // Cerrar el modal
                resetForm();
            }
        } catch (err) {
            toast.error(`Error: ${err.message}`);
        }
    };

    // Confirmación para agregar el producto con un código de barras repetido
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
            precio_venta_ars: '',
            precio_venta_usd: '',
            id_marca: '',
            id_categoria: '',
            codigo_barras: '',
            estado: 'Activo', // Restablecer estado a 'Activo'
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
