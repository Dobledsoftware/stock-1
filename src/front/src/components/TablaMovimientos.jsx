import React, { useState } from 'react';

const TablaMovimientos = ({ productos, onActualizarProducto, onConfirmarMovimientos }) => {
    const actualizarCampo = (id, campo, valor) => {
        onActualizarProducto(id, campo, valor);
    };

    return (
        <div>
            <table>
                <thead>
                    <tr>
                        <th>Producto</th>
                        <th>Cantidad</th>
                        <th>Operación</th>
                        <th>Observaciones</th>
                        <th>Acción</th>
                    </tr>
                </thead>
                <tbody>
                    {productos.map((producto) => (
                        <tr key={producto.id_producto}>
                            <td>{producto.producto_nombre}</td>
                            <td>
                                <input
                                    type="number"
                                    value={producto.cantidad}
                                    onChange={(e) => actualizarCampo(producto.id_producto, 'cantidad', e.target.value)}
                                />
                            </td>
                            <td>
                                <select
                                    value={producto.operacion}
                                    onChange={(e) => actualizarCampo(producto.id_producto, 'operacion', e.target.value)}
                                >
                                    <option value="incrementar">Incrementar</option>
                                    <option value="decrementar">Decrementar</option>
                                </select>
                            </td>
                            <td>
                                <input
                                    type="text"
                                    value={producto.observaciones}
                                    onChange={(e) => actualizarCampo(producto.id_producto, 'observaciones', e.target.value)}
                                />
                            </td>
                            <td>
                                <button onClick={() => onConfirmarMovimientos()}>Confirmar</button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default TablaMovimientos;
