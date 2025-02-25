import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import Swal from 'sweetalert2';
import Estantes from './Estante'; // Importar Estantes

const Almacenes = ({ apiBaseUrl }) => {
    const [almacenes, setAlmacenes] = useState([]);
    const [descripcion, setDescripcion] = useState('');
    const [estado, setEstado] = useState(true);
    const [editandoAlmacen, setEditandoAlmacen] = useState(null);
    const [modalAbierto, setModalAbierto] = useState(false);
    const [almacenSeleccionado, setAlmacenSeleccionado] = useState(null); // Guardar el almacén seleccionado

    // Fetch inicial para listar almacenes
    const fetchAlmacenes = async (estado = true) => {
        try {
            const response = await fetch(
                `${import.meta.env.VITE_API_BASE_URL}/almacen?estado=true`,
                {
                  method: "GET",
                  headers: {
                    "Content-Type": "application/json",
                  },
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
        }
    };

    useEffect(() => {
        fetchAlmacenes();
    }, [apiBaseUrl]);

    // Función para abrir el modal de estantes
    const abrirModalEstantes = (almacen) => {
        setAlmacenSeleccionado(almacen); // Guardar el almacén seleccionado
        setModalAbierto(true); // Abrir el modal
    };

    // Función para cerrar el modal de estantes
    const cerrarModalEstantes = () => {
        setModalAbierto(false); // Cerrar el modal
        setAlmacenSeleccionado(null); // Limpiar el almacén seleccionado
    };

    // Función para abrir el modal de agregar almacen
    const abrirModalAgregarAlmacen = () => {
        setEditandoAlmacen(null); // No estamos editando un almacén
        setModalAbierto(true); // Abrir el modal
    };

    // Función para cerrar el modal de agregar almacen
    const cerrarModalAgregarAlmacen = () => {
        setModalAbierto(false); // Cerrar el modal
        setDescripcion(''); // Limpiar el campo
    };

    // Función para guardar un nuevo almacén
    const handleGuardarAlmacen = async (e) => {
        e.preventDefault();
        const accion = editandoAlmacen ? 'editarAlmacen' : 'agregarAlmacen';
        const body = editandoAlmacen
            ? {
                  accion,
                  id_almacen: editandoAlmacen.id_almacen,
                  descripcion,
                  estado,
              }
            : {
                  accion,
                  descripcion,
                  estado,
              };

        try {
            const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/almacen`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(body),
            });

            if (response.ok) {
                const { status, message } = await response.json();
                Swal.fire({
                    icon: status === 'warning' ? 'warning' : 'success',
                    title: message,
                    showConfirmButton: false,
                    timer: 1500,
                });
                setDescripcion('');
                setEditandoAlmacen(null);
                fetchAlmacenes(); // Recargar los almacenes
                cerrarModalAgregarAlmacen(); // Cerrar modal
            } else {
                throw new Error('Error al guardar el Almacén.');
            }
        } catch (err) {
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: err.message,
            });
        }
    };

    return (
        <div className="almacenes-container">
            <h2>Listado de Almacenes</h2>
            <button onClick={abrirModalAgregarAlmacen}>
                <i className="fa fa-plus"></i> Agregar Almacén
            </button>

            <div className="almacenes-table-container">
                <table id="almacenesTable" className="display">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Descripción</th>
                            <th>Estado</th>
                            <th>Acciones</th>
                        </tr>
                    </thead>
                    <tbody>
                        {almacenes.map((almacen) => (
                            <tr key={almacen.id_almacen}>
                                <td>{almacen.id_almacen}</td>
                                <td>{almacen.descripcion}</td>
                                <td>{almacen.estado ? 'Activo' : 'Inactivo'}</td>
                                <td>
                                    <button onClick={() => abrirModalEstantes(almacen)}>
                                        <i className="fa fa-box"></i> Estantes
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            {/* Modal para agregar almacén */}
            {modalAbierto && !almacenSeleccionado && (
                <div className="modal">
                    <div className="modal-content">
                        <h3>{editandoAlmacen ? 'Editar Almacén' : 'Agregar Almacén'}</h3>
                        <form onSubmit={handleGuardarAlmacen}>
                            <input
                                type="text"
                                placeholder="Descripción del Almacén"
                                value={descripcion}
                                onChange={(e) => setDescripcion(e.target.value)}
                                required
                            />
                            <button type="submit">
                                {editandoAlmacen ? 'Guardar Cambios' : 'Agregar Almacén'}
                            </button>
                        </form>
                        <button onClick={cerrarModalAgregarAlmacen}>Cerrar</button>
                    </div>
                </div>
            )}

            {/* Modal para estantes */}
            {modalAbierto && almacenSeleccionado && (
                <div className="modal">
                    <div className="modal-content">
                        <h3>Estantes de Almacén {almacenSeleccionado.id_almacen}</h3>
                        <Estantes
                            apiBaseUrl={apiBaseUrl}
                            id_almacen={almacenSeleccionado.id_almacen}
                            estado={true} // Aquí le pasas el estado como parámetro
                        />
                        <button onClick={cerrarModalEstantes}>Cerrar</button>
                    </div>
                </div>
            )}
        </div>
    );
};

Almacenes.propTypes = {
    apiBaseUrl: PropTypes.string.isRequired,
};

export default Almacenes;
