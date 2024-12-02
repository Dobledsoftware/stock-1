import React, { useEffect, useState } from 'react';

const TablaProductos = () => {
    const [productos, setProductos] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const obtenerProductos = async () => {
            try {
                const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/producto`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        accion: 'verTodosLosProductos',
                        estado: 'true', // Puede ser 'true' o 'false' dependiendo de los productos que quieras ver
                        id_producto: '', // Si necesitas filtrar por un ID específico, ponlo aquí
                    }),
                });

                const data = await response.json();

                // Verifica si hay datos en la respuesta y actualiza el estado
                if (data.data) {
                    setProductos(data.data);
                } else {
                    console.error('Error al obtener productos:', data.error);
                }
            } catch (error) {
                console.error('Error en la solicitud:', error);
            } finally {
                setLoading(false);
            }
        };

        obtenerProductos();
    }, []);

    if (loading) {
        return <div>Cargando productos...</div>;
    }

    return (
        <div>
            <h2>Lista de Productos</h2>
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Nombre</th>
                        <th>Descripción</th>
                        <th>Precio</th>
                        <th>Stock</th>
                        <th>Proveedor</th>
                        <th>Acciones</th>
                    </tr>
                </thead>
                <tbody>
                    {productos.map((producto) => (
                        <tr key={producto.producto_id}>
                            <td>{producto.producto_id}</td>
                            <td>{producto.producto_nombre}</td>
                            <td>{producto.producto_descripcion}</td>
                            <td>{producto.producto_precio}</td>
                            <td>{producto.producto_stock}</td>
                            <td>{producto.proveedor_nombre}</td>
                            <td>
                                {/* Aquí podrías agregar botones para editar y eliminar productos */}
                                <button>Editar</button>
                                <button>Eliminar</button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default TablaProductos;
