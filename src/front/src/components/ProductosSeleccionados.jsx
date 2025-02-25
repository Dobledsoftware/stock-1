import React, { useState, useEffect } from 'react';
import { toast } from "react-toastify";
import "../styles/ProductosSeleccionados.css";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

const ProductosSeleccionados = ({ productos, onActualizarProducto, onEliminarProducto }) => {
    const [loading, setLoading] = useState(false);
    const [proveedores, setProveedores] = useState([]);
    const [almacenes, setAlmacenes] = useState([]);
    const [estantes, setEstantes] = useState({});
    const [almacenSeleccionado, setAlmacenSeleccionado] = useState(null);

    useEffect(() => {
        cargarProveedores();
        fetchAlmacenes();
    }, []);

    useEffect(() => {
        if (almacenSeleccionado) {
            cargarEstantes(almacenSeleccionado);
        }
    }, [almacenSeleccionado]);

    const fetchData = async (endpoint) => {
        try {
            const response = await fetch(`${API_BASE_URL}/${endpoint}`, {
                method: 'GET',
                headers: { 'Content-Type': 'application/json' }
            });
            if (!response.ok) {
                throw new Error(`Error ${response.status}: ${response.statusText}`);
            }
            const result = await response.json();
            return result.data || [];
        } catch (error) {
            console.error("Error obteniendo datos:", error);
            toast.error(`Error cargando datos de ${endpoint}`);
            return [];
        }
    };

    const cargarProveedores = async () => {
        setLoading(true);
        const data = await fetchData("proveedores?estado=true");
        setProveedores(data);
        setLoading(false);
    };

    const fetchAlmacenes = async () => {
        try {
            const response = await fetch(
                `${API_BASE_URL}/almacen?estado=true`,
                {
                    method: "GET",
                    headers: { "Content-Type": "application/json" },
                }
            );
            if (response.ok) {
                const { data } = await response.json();
                setAlmacenes(data);
            } else {
                throw new Error('Error al listar almacenes.');
            }
        } catch (err) {
            console.error(err.message);
            toast.error('Error al cargar almacenes.');
        }
    };

    const cargarEstantes = async (idAlmacen) => {
        if (!idAlmacen) return;
        setLoading(true);
        const data = await fetchData(`almacen_estante?id_almacen=${idAlmacen}&estado=true`);
        setEstantes(prev => ({ ...prev, [idAlmacen]: data }));
        setLoading(false);
    };

    return (
        <div className="productos-container">
            <h2>Productos Seleccionados</h2>
            {productos.length === 0 ? (
                <p>No hay productos seleccionados.</p>
            ) : (
                <table className="productos-table">
                    <thead>
                        <tr>
                            <th>Producto</th>
                            <th>Cantidad</th>
                            <th>Descripción</th>
                            <th>Proveedor</th>
                            <th>Almacén</th>
                            <th>Estante</th>
                            <th>Acciones</th>
                        </tr>
                    </thead>
                    <tbody>
                        {productos.map((producto) => (
                            <tr key={producto.id_producto}>
                                <td>{producto.producto_nombre}</td>
                                <td>
                                    <input
                                        type="number"
                                        min="1"
                                        value={producto.cantidad}
                                        onChange={(e) => onActualizarProducto(producto.id_producto, "cantidad", e.target.value)}
                                    />
                                </td>
                                <td>
                                    <input
                                        type="text"
                                        value={producto.descripcion}
                                        onChange={(e) => onActualizarProducto(producto.id_producto, "descripcion", e.target.value)}
                                    />
                                </td>
                                <td>
                                    <select onChange={(e) => onActualizarProducto(producto.id_producto, "proveedor", e.target.value)}>
                                        <option value="">Selecciona un proveedor</option>
                                        {proveedores.map((p) => (
                                            <option key={p.id_proveedor} value={p.id_proveedor}>{p.nombre}</option>
                                        ))}
                                    </select>
                                </td>
                                <td>
                                    <select onChange={(e) => { 
                                        onActualizarProducto(producto.id_producto, "almacen", e.target.value);
                                        setAlmacenSeleccionado(e.target.value);
                                    }}>
                                        <option value="">Selecciona un almacén</option>
                                        {almacenes.map((a) => (
                                            <option key={a.id_almacen} value={a.id_almacen}>{a.descripcion}</option>
                                        ))}
                                    </select>
                                </td>
                                <td>
                                    <select onChange={(e) => onActualizarProducto(producto.id_producto, "estante", e.target.value)}>
                                        <option value="">Selecciona un estante</option>
                                        {(estantes[almacenSeleccionado] || []).map((e) => (
                                            <option key={e.id_estante} value={e.id_estante}>{e.descripcion}</option>
                                        ))}
                                    </select>
                                </td>
                                <td>
                                    <button className="delete-btn" onClick={() => onEliminarProducto(producto.id_producto)}>❌</button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}
        </div>
    );
};

export default ProductosSeleccionados;
