import React, { useState, useEffect } from 'react';
import BuscarProductos from '../components/BuscarProductos';
import ProductosSeleccionados from '../components/ProductosSeleccionados';
import { toast } from 'react-toastify';

const Abastecimiento = () => {
    const [productosSeleccionados, setProductosSeleccionados] = useState([]);
    const [proveedores, setProveedores] = useState([]);
    const [almacenes, setAlmacenes] = useState([]);
    const [estantes, setEstantes] = useState([]);
    const [proveedorSeleccionado, setProveedorSeleccionado] = useState(null);
    const [almacenSeleccionado, setAlmacenSeleccionado] = useState(null);
    const [estanteSeleccionado, setEstanteSeleccionado] = useState(null);
    const [loading, setLoading] = useState(false);
    const [mostrarModal, setMostrarModal] = useState(false);

    useEffect(() => {
        cargarDatosIniciales();
    }, []);

    useEffect(() => {
        if (almacenSeleccionado) cargarEstantes(almacenSeleccionado);
    }, [almacenSeleccionado]);

    const cargarDatosIniciales = async () => {
        setLoading(true);
        try {
            const [proveedoresData, almacenesData] = await Promise.all([
                fetchData('/proveedores', { estado: true }),
                fetchData('/almacen', { estado: true })
            ]);
            setProveedores(proveedoresData);
            setAlmacenes(almacenesData);
        } catch (error) {
            toast.error('Error al cargar proveedores y almacenes.');
        } finally {
            setLoading(false);
        }
    };

    const cargarEstantes = async (idAlmacen) => {
        setLoading(true);
        try {
            const data = await fetchData('/estante', { id_almacen: idAlmacen, estado: true });
            setEstantes(data);
        } catch (error) {
            toast.error('Error al cargar estantes.');
        } finally {
            setLoading(false);
        }
    };

    const fetchData = async (endpoint, params = {}) => {
        try {
            const queryString = new URLSearchParams(params).toString();
            const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}${endpoint}?${queryString}`);
            if (!response.ok) throw new Error(`Error ${response.status}: ${response.statusText}`);
            const data = await response.json();
            return data.data || [];
        } catch (error) {
            console.error('Error en la solicitud:', error);
            toast.error(`Error en la solicitud a ${endpoint}`);
            return [];
        }
    };

    const procesarMovimiento = async () => {
        console.log("Procesando movimiento", productosSeleccionados);
        if (!productosSeleccionados.length) {
            toast.warning('Debe seleccionar al menos un producto.');
            return;
        }
        if (!proveedorSeleccionado || !almacenSeleccionado || !estanteSeleccionado) {
            toast.warning('Debe seleccionar proveedor, almacén y estante.');
            return;
        }

        if (!window.confirm('¿Está seguro de procesar el movimiento?')) {
            return;
        }

        const movimientos = productosSeleccionados.map(p => ({
            id_producto: p.id_producto,
            cantidad: p.cantidad,
            id_tipo_movimiento: 1, 
            id_usuario: 1, 
            id_proveedor: proveedorSeleccionado,
            id_almacen: almacenSeleccionado,
            id_estante: estanteSeleccionado,
            descripcion: p.descripcion || ""
        }));

        setLoading(true);
        try {
            fetch(`${import.meta.env.VITE_API_BASE_URL}/movimiento_stock`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ movimientos })
            })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(errorData => { throw new Error(errorData.message || 'Error al procesar el movimiento de stock'); });
                }
                return response.json();
            })
            .then(data => {
                console.log("Respuesta del servidor:", data);
                toast.success('Movimiento procesado exitosamente');
                setProductosSeleccionados([]);
            })
            .catch(error => {
                console.error('Error en el procesamiento:', error);
                toast.error('Hubo un problema al enviar los datos. Verifique los valores.');
            })
            .finally(() => setLoading(false));
        } catch (error) {
            console.error('Error inesperado:', error);
            toast.error('Error inesperado en la solicitud.');
            setLoading(false);
        }
    };

    return (
        <div className="container">
            <h1>Abastecimiento de Stock</h1>
            <button className="btn-primary" onClick={() => setMostrarModal(true)}>Buscar Productos</button>

            {mostrarModal && (
                <div className="modal">
                    <div className="modal-content">
                        <button className="close-btn" onClick={() => setMostrarModal(false)}>×</button>
                        <div className="modal-body">
                            <BuscarProductos onAgregarProducto={(producto) => setProductosSeleccionados([...productosSeleccionados, producto])} />
                        </div>
                    </div>
                </div>
            )}

            <ProductosSeleccionados
                productos={productosSeleccionados}
                onEliminarProducto={(id) => setProductosSeleccionados(productosSeleccionados.filter(p => p.id_producto !== id))}
                onActualizarProducto={(id, campo, valor) => setProductosSeleccionados(productosSeleccionados.map(p => p.id_producto === id ? { ...p, [campo]: valor } : p))}
            />

            <button className="btn-success" onClick={procesarMovimiento} disabled={loading}>
                {loading ? 'Procesando...' : 'Procesar Movimiento'}
            </button>

            {loading && <p>Cargando...</p>}
        </div>
    );
};

export default Abastecimiento;
