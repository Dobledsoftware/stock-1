import { useState } from 'react';

const BuscarProductos = ({ onAgregarProducto }) => {
    const [busqueda, setBusqueda] = useState('');
    const [productosEncontrados, setProductosEncontrados] = useState([]);
    const [mostrarAlerta, setMostrarAlerta] = useState(false);
    const [cargando, setCargando] = useState(false);
    const [paginaActual, setPaginaActual] = useState(1);
    const productosPorPagina = 10; // Tamaño de página configurable

    const buscarProducto = async () => {
        if (!busqueda.trim()) {
            setMostrarAlerta(true);
            return;
        }
        setMostrarAlerta(false);
        setCargando(true); // Mostrar indicador de carga
        try {
            const response = await fetch(
                `${import.meta.env.VITE_API_BASE_URL}/productos?estado=true`,
                {
                  method: "GET",
                  headers: {
                    "Content-Type": "application/json",
                  },
                }
              );

            if (!response.ok) {
                throw new Error(`Error en la respuesta del servidor: ${response.status} ${response.statusText}`);
            }

            const data = await response.json();

            if (Array.isArray(data.data)) {
                const productosFiltrados = data.data.filter((producto) =>
                    (producto.producto_nombre && producto.producto_nombre.toLowerCase().includes(busqueda.toLowerCase())) ||
                    (producto.producto_marca && producto.producto_marca.toLowerCase().includes(busqueda.toLowerCase())) ||
                    (producto.producto_codigo_barras && producto.producto_codigo_barras.includes(busqueda))
                );
                setProductosEncontrados(productosFiltrados);
                setPaginaActual(1);
                setBusqueda(''); // Limpiar el campo de búsqueda
            } else {
                console.error('La respuesta de la API no contiene un arreglo en la propiedad "data":', data);
                alert('Hubo un problema al obtener los productos.');
            }
        } catch (error) {
            console.error('Error al obtener productos:', error);
            alert(`Error al obtener productos: ${error.message}`);
        } finally {
            setCargando(false); // Ocultar indicador de carga
        }
    };

    // Manejo del evento Enter para lectores de código de barras
    const manejarEnter = (e) => {
        if (e.key === 'Enter') {
            buscarProducto();
        }
    };

    // Obtener los productos de la página actual
    const productosPaginados = productosEncontrados.slice(
        (paginaActual - 1) * productosPorPagina,
        paginaActual * productosPorPagina
    );

    const cambiarPagina = (nuevaPagina) => {
        if (nuevaPagina > 0 && nuevaPagina <= Math.ceil(productosEncontrados.length / productosPorPagina)) {
            setPaginaActual(nuevaPagina);
        }
    };

    return (
        <div>
            <input
                type="text"
                value={busqueda}
                onChange={(e) => setBusqueda(e.target.value)}
                placeholder="Buscar producto"
                onKeyDown={manejarEnter} // Detectar Enter
            />
            <button onClick={buscarProducto}>Buscar</button>

            {mostrarAlerta && <p>No se ha ingresado ningún término de búsqueda.</p>}
            {cargando && <p>Cargando productos...</p>}

            {!cargando && productosEncontrados.length === 0 && !mostrarAlerta && <p>No se encontraron productos.</p>}

            {!cargando && productosEncontrados.length > 0 && (
                <div>
                    <table>
                        <thead>
                            <tr>
                                <th>Nombre</th>
                                <th>Marca</th>
                                <th>Código de Barras</th>
                                <th>Acciones</th>
                            </tr>
                        </thead>
                        <tbody>
                            {productosPaginados.map((producto) => (
                                <tr key={producto.producto_id}>
                                    <td>{producto.producto_nombre || 'Sin nombre'}</td>
                                    <td>{producto.producto_marca || 'Sin marca'}</td>
                                    <td>{producto.producto_codigo_barras || 'Sin código de barras'}</td>
                                    <td>
                                        <button onClick={() => onAgregarProducto(producto)}>Agregar</button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>

                    {/* Controles de paginación */}
                    <div>
                        <button
                            onClick={() => cambiarPagina(paginaActual - 1)}
                            disabled={paginaActual === 1}
                        >
                            Anterior
                        </button>
                        <span>
                            Página {paginaActual} de {Math.ceil(productosEncontrados.length / productosPorPagina)}
                        </span>
                        <button
                            onClick={() => cambiarPagina(paginaActual + 1)}
                            disabled={paginaActual === Math.ceil(productosEncontrados.length / productosPorPagina)}
                        >
                            Siguiente
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
};

export default BuscarProductos;
