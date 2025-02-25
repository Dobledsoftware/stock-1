import { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import $ from 'jquery'; // Necesario para DataTables

const Proveedores = ({ apiBaseUrl, onClose }) => {
    const [proveedores, setProveedores] = useState([]);
    const [nombre, setNombre] = useState('');
    const [direccion, setDireccion] = useState('');
    const [telefono, setTelefono] = useState('');
    const [correoContacto, setCorreoContacto] = useState('');
    const [mensaje, setMensaje] = useState('');
    const [error, setError] = useState('');
    const [editandoProveedor, setEditandoProveedor] = useState(null);
    const [modalAbierto, setModalAbierto] = useState(false); // Estado para controlar la visibilidad del modal

    // Fetch inicial para listar proveedores (cambiado a GET)
    const fetchProveedores = async () => {
        try {
            const response = await fetch(
                `${import.meta.env.VITE_API_BASE_URL}/proveedores?estado=true`,
                {
                  method: "GET",
                  headers: {
                    "Content-Type": "application/json",
                  },
                }
              );

            if (response.ok) {
                const { data } = await response.json();
                setProveedores(data);
                setError('');
            } else {
                throw new Error('Error al listar proveedores.');
            }
        } catch (err) {
            setError(err.message);
        }
    };

    // Crear o editar proveedor
    const handleSubmit = async (e) => {
        e.preventDefault();
        const accion = editandoProveedor ? 'editarProveedor' : 'agregarProveedor';
        const body = editandoProveedor
            ? {
                  accion,
                  id_proveedor: editandoProveedor.id_proveedor,
                  nombre,
                  direccion,
                  telefono,
                  correo_contacto: correoContacto,
              }
            : {
                  accion,
                  nombre,
                  direccion,
                  telefono,
                  correo_contacto: correoContacto,
              };

        try {
            const response = await fetch(`${apiBaseUrl}/proveedor`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(body),
            });

            if (response.ok) {
                const data = await response.json();
                if (data.status === 'warning') {
                    setMensaje(data.message);
                } else {
                    setMensaje(`Proveedor ${editandoProveedor ? 'modificado' : 'agregado'} con éxito.`);
                }
                setError('');
                setNombre('');
                setDireccion('');
                setTelefono('');
                setCorreoContacto('');
                setEditandoProveedor(null);
                fetchProveedores();
                setModalAbierto(false); // Cerrar modal después de la acción
            } else {
                throw new Error('Error al guardar el proveedor.');
            }
        } catch (err) {
            setError(err.message);
        }
    };

    // Seleccionar un proveedor para edición
    const handleEditar = (proveedor) => {
        setEditandoProveedor(proveedor);
        setNombre(proveedor.nombre);
        setDireccion(proveedor.direccion);
        setTelefono(proveedor.telefono);
        setCorreoContacto(proveedor.correo_contacto);
        setModalAbierto(true); // Abrir modal para editar
    };

    // Abrir el modal para agregar un nuevo proveedor
    const abrirModalAgregar = () => {
        setNombre('');
        setDireccion('');
        setTelefono('');
        setCorreoContacto('');
        setEditandoProveedor(null);
        setModalAbierto(true); // Abrir modal para agregar
    };

    useEffect(() => {
        fetchProveedores();
    }, [apiBaseUrl]);

    // Inicializar DataTable
    useEffect(() => {
        if (proveedores.length > 0) {
            $('#proveedoresTable').DataTable({
                pageLength: 10,
                lengthChange: false,
                searching: true,
                ordering: true,
                info: true,
            });
        }
    }, [proveedores]);

    return (
        <div className="proveedores-container">
            <h2>Listado de Proveedores</h2>
            <button onClick={abrirModalAgregar}>
                <i className="fa fa-plus"></i> Agregar Proveedor
            </button>

            <div className="proveedores-table-container">
                <table id="proveedoresTable" className="display">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Nombre</th>
                            <th>Dirección</th>
                            <th>Teléfono</th>
                            <th>Correo</th>
                            <th>Acciones</th>
                        </tr>
                    </thead>
                    <tbody>
                        {proveedores.map((proveedor) => (
                            <tr key={proveedor.id_proveedor}>
                                <td>{proveedor.id_proveedor}</td>
                                <td>{proveedor.nombre}</td>
                                <td>{proveedor.direccion}</td>
                                <td>{proveedor.telefono}</td>
                                <td>{proveedor.correo_contacto}</td>
                                <td>
                                    <button onClick={() => handleEditar(proveedor)}>
                                        <i className="fa fa-pencil"></i> Editar
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            {/* Modal para agregar o editar proveedor */}
            {modalAbierto && (
                <div className="modal">
                    <div className="modal-content">
                        <h3>{editandoProveedor ? 'Editar Proveedor' : 'Agregar Proveedor'}</h3>
                        <form onSubmit={handleSubmit}>
                            <input
                                type="text"
                                placeholder="Nombre"
                                value={nombre}
                                onChange={(e) => setNombre(e.target.value)}
                                required
                            />
                            <input
                                type="text"
                                placeholder="Dirección"
                                value={direccion}
                                onChange={(e) => setDireccion(e.target.value)}
                                required
                            />
                            <input
                                type="tel"
                                placeholder="Teléfono"
                                value={telefono}
                                onChange={(e) => setTelefono(e.target.value)}
                                required
                            />
                            <input
                                type="email"
                                placeholder="Correo de Contacto"
                                value={correoContacto}
                                onChange={(e) => setCorreoContacto(e.target.value)}
                                required
                            />
                            <button type="submit">
                                {editandoProveedor ? 'Guardar Cambios' : 'Agregar'}
                            </button>
                            <button type="button" onClick={() => setModalAbierto(false)}>
                                Cancelar
                            </button>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
};

Proveedores.propTypes = {
    apiBaseUrl: PropTypes.string.isRequired,
    onClose: PropTypes.func.isRequired,
};

export default Proveedores;
