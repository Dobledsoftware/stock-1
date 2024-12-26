import React, { useState } from 'react';
import { FaSearch, FaPlus, FaTrash } from 'react-icons/fa'; // Importación de íconos
import '../styles/abastecimiento.module.css';

const Abastecimiento = () => {
    const [productosEncontrados, setProductosEncontrados] = useState([]);
    const [tablaTrabajo, setTablaTrabajo] = useState([]);
    const [busqueda, setBusqueda] = useState('');
    const [accion, setAccion] = useState('');
    const [motivo, setMotivo] = useState('');
    const [mostrarResultados, setMostrarResultados] = useState(false);

    const buscarProducto = async () => {
        if (!accion) {
            alert('Por favor, selecciona una acción.');
            return;
        }
        if (!motivo.trim()) {
            alert('Por favor, ingresa un motivo.');
            return;
        }

        setProductosEncontrados([]);

        try {
            const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/producto`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    accion: 'verTodosLosProductos',
                    estado: 'Activo',
                }),
            });

            const data = await response.json();

            if (Array.isArray(data.data)) {
                const resultados = data.data.filter((prod) => {
                    const nombre = prod.producto_nombre ? prod.producto_nombre.toLowerCase() : '';
                    const marca = prod.producto_marca ? prod.producto_marca.toLowerCase() : '';
                    const codigoBarras = prod.producto_codigo_barras ? prod.producto_codigo_barras.toLowerCase() : '';
                    return (
                        nombre.includes(busqueda.toLowerCase()) ||
                        marca.includes(busqueda.toLowerCase()) ||
                        codigoBarras.includes(busqueda.toLowerCase())
                    );
                });
                

                setMostrarResultados(true);
                setProductosEncontrados(resultados);
            } else {
                console.error('La respuesta de la API no contiene un arreglo en la propiedad "data":', data);
                alert('Hubo un problema al obtener los productos.');
            }

            setBusqueda('');
            setAccion('');
            setMotivo('');
        } catch (error) {
            console.error('Error al obtener productos:', error);
            alert('Hubo un error al obtener los productos.');
        }
    };
   
    
    const agregarATabla = (producto) => {
        if (!tablaTrabajo.some((p) => p.producto_id === producto.producto_id)) {
            setTablaTrabajo([...tablaTrabajo, { ...producto, cantidad: 0 }]);
        }
    };

    const actualizarCantidad = (id, nuevaCantidad) => {
        setTablaTrabajo((prev) =>
            prev.map((prod) =>
                prod.producto_id === id ? { ...prod, cantidad: nuevaCantidad } : prod
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
        setMostrarResultados(false);
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
                    onKeyDown={(e) => e.key === 'Enter' && buscarProducto()} // Detecta "Enter"
                />
                <button onClick={buscarProducto}>
                    <FaSearch /> Buscar
                </button>
            </div>

            {/* Resultados de búsqueda */}
            <div className="resultados">
                <h2>Resultados de la búsqueda</h2>
                {mostrarResultados ? (
                    <table>
                        <thead>
                            <tr>
                                <th>Nombre</th>
                                <th>Marca</th>
                                <th>Código de Barras</th>
                                <th>Acción</th>
                            </tr>
                        </thead>
                        <tbody>
                            {productosEncontrados.map((producto) => (
                                <tr key={producto.producto_id}>
                                    <td>{producto.producto_nombre}</td>
                                    <td>{producto.producto_marca}</td>
                                    <td>{producto.producto_codigo_barras}</td>
                                    <td>
                                        <button onClick={() => agregarATabla(producto)}>
                                            <FaPlus /> Agregar
                                        </button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                ) : (
                    <p>No se han encontrado productos.</p>
                )}
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
                                <tr key={producto.producto_id}>
                                    <td>{producto.producto_nombre}</td>
                                    <td>
                                        <input
                                            type="number"
                                            value={producto.cantidad}
                                            onChange={(e) =>
                                                actualizarCantidad(producto.producto_id, parseInt(e.target.value) || 0)
                                            }
                                        />
                                    </td>
                                    <td>
                                        <button
                                            onClick={() =>
                                                setTablaTrabajo((prev) =>
                                                    prev.filter((p) => p.producto_id !== producto.producto_id)
                                                )
                                            }>
                                            <FaTrash /> Eliminar
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
