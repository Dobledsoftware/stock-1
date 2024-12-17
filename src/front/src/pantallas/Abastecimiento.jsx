import React, { useState } from 'react';
import '../styles/abastecimiento.css';

const Abastecimiento = () => {
    const [productosEncontrados, setProductosEncontrados] = useState([]); // Lista de productos encontrados
    const [tablaTrabajo, setTablaTrabajo] = useState([]); // Productos en la tabla de trabajo
    const [busqueda, setBusqueda] = useState(''); // Texto del buscador
    const [accion, setAccion] = useState(''); // Aumentar o Disminuir
    const [motivo, setMotivo] = useState(''); // Motivo de la acción

    const buscarProducto = () => {
        // Validar que se haya seleccionado una acción y proporcionado un motivo
        if (!accion) {
            alert('Por favor, selecciona una acción: Aumentar o Disminuir.');
            return;
        }
        if (!motivo.trim()) {
            alert('Por favor, ingresa un motivo para la acción.');
            return;
        }

        // Simula buscar productos en una base de datos o API
        const productosMock = [
            { id: 1, nombre: 'Producto A', stock: 10 },
            { id: 2, nombre: 'Producto B', stock: 20 },
        ];

        const resultados = productosMock.filter((prod) =>
            prod.nombre.toLowerCase().includes(busqueda.toLowerCase())
        );
        setProductosEncontrados(resultados);
    };

    const agregarATabla = (producto) => {
        if (!tablaTrabajo.some((p) => p.id === producto.id)) {
            setTablaTrabajo([...tablaTrabajo, { ...producto, cantidad: 0 }]);
        }
    };

    const actualizarCantidad = (id, nuevaCantidad) => {
        setTablaTrabajo((prev) =>
            prev.map((prod) =>
                prod.id === id ? { ...prod, cantidad: nuevaCantidad } : prod
            )
        );
    };

    const confirmarAbastecimiento = () => {
        if (!tablaTrabajo.length) {
            alert('No hay productos en la tabla para confirmar.');
            return;
        }

        const datosAEnviar = {
            accion,
            motivo,
            productos: tablaTrabajo,
        };

        console.log('Datos enviados al backend:', datosAEnviar);
        alert('Datos enviados correctamente.');
        setTablaTrabajo([]);
        setProductosEncontrados([]);
        setBusqueda('');
        setMotivo('');
        setAccion('');
    };

    return (
        <div className="abastecimiento">
            <h1>Movimiento de stock</h1>

            {/* Selección de Acción y Motivo */}
            <div className="acciones">
                <select value={accion} onChange={(e) => setAccion(e.target.value)}>
                    <option value="">Seleccionar acción</option>
                    <option value="aumentar">Entrada Stock</option>
                    <option value="disminuir">Salida Stock</option>
                </select>
                <input
                    type="text"
                    placeholder="Motivo de la acción"
                    value={motivo}
                    onChange={(e) => setMotivo(e.target.value)}
                />
            </div>

            {/* Buscador */}
            <div className="buscador">
                <input
                    type="text"
                    placeholder="Buscar producto..."
                    value={busqueda}
                    onChange={(e) => setBusqueda(e.target.value)}
                />
                <button onClick={buscarProducto}>Buscar</button>
            </div>

            {/* Resultados de búsqueda */}
            <div className="resultados">
                <h2>Resultados de la búsqueda</h2>
                <ul>
                    {productosEncontrados.map((producto) => (
                        <li key={producto.id}>
                            {producto.nombre} (Stock: {producto.stock})
                            <button onClick={() => agregarATabla(producto)}>Agregar</button>
                        </li>
                    ))}
                </ul>
            </div>

            {/* Tabla de trabajo */}
            <div className="tabla-trabajo">
                <h2>Tabla de Trabajo</h2>
                {tablaTrabajo.length > 0 ? (
                    <table>
                        <thead>
                            <tr>
                                <th>Producto</th>
                                <th>Cantidad</th>
                                <th>Acciones</th>
                            </tr>
                        </thead>
                        <tbody>
                            {tablaTrabajo.map((producto) => (
                                <tr key={producto.id}>
                                    <td>{producto.nombre}</td>
                                    <td>
                                        <input
                                            type="number"
                                            value={producto.cantidad}
                                            onChange={(e) =>
                                                actualizarCantidad(
                                                    producto.id,
                                                    parseInt(e.target.value) || 0
                                                )
                                            }
                                        />
                                    </td>
                                    <td>
                                        <button
                                            onClick={() =>
                                                setTablaTrabajo((prev) =>
                                                    prev.filter((p) => p.id !== producto.id)
                                                )
                                            }
                                        >
                                            Eliminar
                                        </button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                ) : (
                    <p>No hay productos en la tabla de trabajo.</p>
                )}
            </div>

            {/* Botón para confirmar */}
            {tablaTrabajo.length > 0 && (
                <button onClick={confirmarAbastecimiento} className="btn-confirmar">
                    Confirmar Abastecimiento
                </button>
            )}
        </div>
    );
};

export default Abastecimiento;
