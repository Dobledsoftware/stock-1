import React, { useState, useEffect } from 'react';
import BuscarProductos from '../components/BuscarProductos';
import ProductosSeleccionados from '../components/ProductosSeleccionados';

const Abastecimiento = () => {
    const [productosSeleccionados, setProductosSeleccionados] = useState([]);
    const [proveedores, setProveedores] = useState([]);
    const [almacenes, setAlmacenes] = useState([]);
    const [estantes, setEstantes] = useState([]);
    const [proveedorSeleccionado, setProveedorSeleccionado] = useState(null);
    const [almacenSeleccionado, setAlmacenSeleccionado] = useState(null);
    const [estanteSeleccionado, setEstanteSeleccionado] = useState(null);

    // Cargar listas desplegables al montar
    useEffect(() => {
        const fetchProveedores = async () => {
            const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/proveedor`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ accion: 'verTodosLosProveedores', estado: true }),
            });
            const data = await response.json();
            setProveedores(data.data || []);
        };

        const fetchAlmacenes = async () => {
            const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/almacen`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ accion: 'verTodosLosAlmacenes', estado: true }),
            });
            const data = await response.json();
            setAlmacenes(data.data || []);
        };

        fetchProveedores();
        fetchAlmacenes();
    }, []);

    // Cargar estantes cuando se selecciona un almacén
    useEffect(() => {
        const fetchEstantes = async () => {
            if (almacenSeleccionado) {
                const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/estante`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        accion: 'verTodosLosEstantes',
                        id_almacen: almacenSeleccionado,
                        estado: true,
                    }),
                });
                const data = await response.json();
                setEstantes(data.data || []);
            }
        };

        fetchEstantes();
    }, [almacenSeleccionado]);

    // Agregar un producto a la lista de movimientos
    const agregarProducto = (producto) => {
        if (!productosSeleccionados.find((p) => p.id_producto === producto.producto_id)) {
            setProductosSeleccionados([
                ...productosSeleccionados,
                {
                    id_producto: producto.producto_id,
                    producto_nombre: producto.producto_nombre,
                    cantidad: 0,
                    descripcion: '',
                },
            ]);
        }
    };

    // Eliminar un producto de la lista de movimientos
    const eliminarProducto = (idProducto) => {
        setProductosSeleccionados(productosSeleccionados.filter((p) => p.id_producto !== idProducto));
    };

    // Manejar el cambio de valores (cantidad y descripción) en la lista
    const actualizarProducto = (idProducto, campo, valor) => {
        setProductosSeleccionados(
            productosSeleccionados.map((p) =>
                p.id_producto === idProducto ? { ...p, [campo]: valor } : p
            )
        );
    };

    // Enviar el JSON al backend
    const procesarMovimiento = async () => {
        if (!proveedorSeleccionado || !almacenSeleccionado || !estanteSeleccionado) {
            alert('Debes seleccionar un proveedor, almacén y estante.');
            return;
        }

        const movimientos = productosSeleccionados.map((p) => ({
            id_producto: p.id_producto,
            cantidad: p.cantidad,
            operacion: 'incrementar',
            id_usuario: 123, // Aquí se debe reemplazar con el usuario real
            observaciones: 'Reabastecimiento',
            id_proveedor: proveedorSeleccionado,
            id_almacen: almacenSeleccionado,
            id_estante: estanteSeleccionado,
            descripcion: p.descripcion,
        }));

        const payload = { movimientos };

        try {
            const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/movimientos`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload),
            });

            if (!response.ok) {
                throw new Error('Error al procesar el movimiento');
            }

            alert('Movimiento procesado con éxito');
            setProductosSeleccionados([]); // Limpiar la lista
        } catch (error) {
            console.error('Error al enviar el movimiento:', error);
            alert('Hubo un problema al procesar el movimiento.');
        }
    };

    return (
        <div>
            <h1>Abastecimiento de Stock</h1>

            {/* Buscador */}
            <BuscarProductos onAgregarProducto={agregarProducto} />

            {/* Listas desplegables */}
            <div>
                <select onChange={(e) => setProveedorSeleccionado(e.target.value)} value={proveedorSeleccionado || ''}>
                    <option value="">Selecciona un proveedor</option>
                    {proveedores.map((p) => (
                        <option key={p.id_proveedor} value={p.id_proveedor}>
                            {p.nombre}
                        </option>
                    ))}
                </select>

                <select onChange={(e) => setAlmacenSeleccionado(e.target.value)} value={almacenSeleccionado || ''}>
                    <option value="">Selecciona un almacén</option>
                    {almacenes.map((a) => (
                        <option key={a.id_almacen} value={a.id_almacen}>
                            {a.nombre}
                        </option>
                    ))}
                </select>

                <select onChange={(e) => setEstanteSeleccionado(e.target.value)} value={estanteSeleccionado || ''}>
                    <option value="">Selecciona un estante</option>
                    {estantes.map((e) => (
                        <option key={e.id_estante} value={e.id_estante}>
                            {e.nombre}
                        </option>
                    ))}
                </select>
            </div>

            {/* Productos seleccionados */}
            <ProductosSeleccionados
                productos={productosSeleccionados}
                onEliminarProducto={eliminarProducto}
                onProcesarPaquete={procesarMovimiento}
            />
        </div>
    );
};

export default Abastecimiento;
