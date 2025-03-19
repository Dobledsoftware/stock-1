import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import '../styles/AgregarProducto.module.css';
import { toast } from 'react-toastify';
import Swal from 'sweetalert2';

const AgregarProducto = ({ onProductoAgregado, onClose }) => {
    const [formData, setFormData] = useState({
        nombre: '',
        descripcion: '',
        precio_venta_ars: '',
        precio_venta_usd: '',
        id_marca: '',
        id_categoria: '',
        codigo_barras: '',
        estado: 'Activo',
        aplicar_incremento_automatico_ars: false,
        aplicar_incremento_automatico_usd: false,
        es_dolar: false,
    });

    const [categorias, setCategorias] = useState([]);
    const [marcas, setMarcas] = useState([]);
    const baseUrl = import.meta.env.VITE_API_BASE_URL;

    useEffect(() => {
        const fetchData = async (url, setState) => {
            try {
                const response = await fetch(url);
                if (!response.ok) throw new Error('Error al obtener datos del servidor');
                const { data } = await response.json();
                setState(data);
            } catch (err) {
                toast.error(`Error: ${err.message}`);
            }
        };

        fetchData(`${baseUrl}/productos_categorias?estado=true`, setCategorias);
        fetchData(`${baseUrl}/producto_marcas?estado=true`, setMarcas);
    }, [baseUrl]);

    const handleInputChange = (e) => {
        const { name, value, type, checked } = e.target;
        setFormData((prev) => ({ ...prev, [name]: type === 'checkbox' ? checked : value }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        const producto = {
            ...formData,
            precio_venta_ars: parseFloat(formData.precio_venta_ars),
            precio_venta_usd: parseFloat(formData.precio_venta_usd),
            id_marca: formData.id_marca ? parseInt(formData.id_marca, 10) : null,
            id_categoria: formData.id_categoria ? parseInt(formData.id_categoria, 10) : null,
            estado: formData.estado === 'Activo',
            forceAdd: false,
        };

        try {
            const response = await fetch(`${baseUrl}/producto`, {
                method: 'POST',
                body: JSON.stringify(producto),
                headers: { 'Content-Type': 'application/json' },
            });
            const { status, message, productos_repetidos } = await response.json();

            if (status === 'warning' && productos_repetidos.length > 0) {
                Swal.fire({
                    title: '¡Advertencia!',
                    text: `Ya existen productos con el código de barras. ¿Desea agregar el producto de todos modos?`,
                    icon: 'warning',
                    showCancelButton: true,
                    confirmButtonText: 'Sí, agregar',
                    cancelButtonText: 'No, cancelar',
                }).then((result) => {
                    if (result.isConfirmed) {
                        agregarProductoConConfirmacion({ ...producto, forceAdd: true });
                    }
                });
            } else {
                Swal.fire({ title: '¡Éxito!', text: message, icon: 'success', confirmButtonText: 'Aceptar' });
                onProductoAgregado();
                onClose();
                resetForm();
            }
        } catch (err) {
            toast.error(`Error: ${err.message}`);
        }
    };

    const agregarProductoConConfirmacion = async (producto) => {
        try {
            const response = await fetch(`${baseUrl}/producto`, {
                method: 'POST',
                body: JSON.stringify(producto),
                headers: { 'Content-Type': 'application/json' },
            });
            const { message } = await response.json();
            Swal.fire({ title: '¡Éxito!', text: message, icon: 'success', confirmButtonText: 'Aceptar' });
            onProductoAgregado();
            onClose();
            resetForm();
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
            estado: 'Activo',
            aplicar_incremento_automatico_ars: false,
            aplicar_incremento_automatico_usd: false,
            es_dolar: false,
        });
    };

    return (
        <div className="modal">
            <div className="modal-content">
                <span className="close" onClick={onClose}>×</span>
                <h2>Agregar producto</h2>
                <form onSubmit={handleSubmit}>
                    {['nombre', 'descripcion', 'precio_venta_ars', 'precio_venta_usd', 'codigo_barras'].map((field) => (
                        <input key={field} type={field.includes('precio') ? 'number' : 'text'} name={field} placeholder={field.replace('_', ' ')} value={formData[field]} onChange={handleInputChange} required />
                    ))}

                    <select name="id_categoria" value={formData.id_categoria} onChange={handleInputChange} required>
                        <option value="" disabled>Seleccionar categoría</option>
                        {categorias?.length > 0 &&
                            categorias.map((categoria) => (
                                <option key={categoria.id_categoria} value={categoria.id_categoria}>{categoria.descripcion}</option>
                            ))}
                    </select>

                    <select name="id_marca" value={formData.id_marca} onChange={handleInputChange} required>
                        <option value="" disabled>Seleccionar marca</option>
                        {marcas?.length > 0 &&
                            marcas.map((marca) => (
                                <option key={marca.id_marca} value={marca.id_marca}>{marca.descripcion}</option>
                            ))}
                    </select>

                    <div className="checkbox-group">
    <label className="checkbox-label">
        <input type="checkbox" name="aplicar_incremento_automatico_ars" checked={formData.aplicar_incremento_automatico_ars} onChange={handleInputChange} />
        Aplicar incremento automático en ARS
    </label><br />
    <label className="checkbox-label">
        <input type="checkbox" name="aplicar_incremento_automatico_usd" checked={formData.aplicar_incremento_automatico_usd} onChange={handleInputChange} />
        Aplicar incremento automático en USD
    </label><br />
    <label className="checkbox-label">
        <input type="checkbox" name="es_dolar" checked={formData.es_dolar} onChange={handleInputChange} />
        Producto en dólares
    </label>
</div>

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
