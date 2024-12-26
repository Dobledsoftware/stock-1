import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import $ from 'jquery'; // Necesario para DataTables
import Swal from 'sweetalert2'; // Importar SweetAlert

const Marcas = ({ apiBaseUrl }) => {
    const [marcas, setMarcas] = useState([]);
    const [descripcion, setDescripcion] = useState('');
    const [estado, setEstado] = useState(true);
    const [editandoMarca, setEditandoMarca] = useState(null);
    const [modalAbierto, setModalAbierto] = useState(false); // Estado para controlar la visibilidad del modal

    // Fetch inicial para listar marcas
    const fetchMarcas = async (incluirInactivas = true) => {
        try {
            const response = await fetch(`${apiBaseUrl}/producto_marca`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    accion: 'verTodasLasMarcas',
                    incluir_inactivas: incluirInactivas,
                }),
            });

            if (response.ok) {
                const { data } = await response.json();
                setMarcas(data);
            } else {
                throw new Error('Error al listar marcas.');
            }
        } catch (err) {
            console.error(err.message);
        }
    };

    // Crear o editar marca
    const handleSubmit = async (e) => {
        e.preventDefault();
        const accion = editandoMarca ? 'modificarMarca' : 'agregarMarca';
        const body = editandoMarca
            ? {
                  accion,
                  id_marca: editandoMarca.id_marca,
                  descripcion,
                  estado,
              }
            : {
                  accion,
                  descripcion,
                  estado,
              };

        try {
            const response = await fetch(`${apiBaseUrl}/producto_marca`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(body),
            });

            if (response.ok) {
                Swal.fire({
                    icon: 'success',
                    title: `Marca ${editandoMarca ? 'modificada' : 'agregada'} con éxito`,
                    showConfirmButton: false,
                    timer: 1500,
                });
                setDescripcion('');
                setEstado(true);
                setEditandoMarca(null);
                setModalAbierto(false);
                fetchMarcas();
            } else {
                throw new Error('Error al guardar la marca.');
            }
        } catch (err) {
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: err.message,
            });
        }
    };

    // Eliminar marca (soft delete)
    const handleEliminar = async (idMarca) => {
        Swal.fire({
            title: '¿Estás seguro?',
            text: "Esta acción no se puede deshacer.",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#d33',
            cancelButtonColor: '#3085d6',
            confirmButtonText: 'Sí, eliminar',
        }).then(async (result) => {
            if (result.isConfirmed) {
                try {
                    const response = await fetch(`${apiBaseUrl}/producto_marca`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            accion: 'eliminarMarca',
                            id_marca: idMarca,
                        }),
                    });

                    if (response.ok) {
                        Swal.fire({
                            icon: 'success',
                            title: 'Marca eliminada con éxito',
                            showConfirmButton: false,
                            timer: 1500,
                        });
                        fetchMarcas();
                    } else {
                        throw new Error('Error al eliminar la marca.');
                    }
                } catch (err) {
                    Swal.fire({
                        icon: 'error',
                        title: 'Error',
                        text: err.message,
                    });
                }
            }
        });
    };

    // Seleccionar una marca para edición
    const handleEditar = (marca) => {
        setEditandoMarca(marca);
        setDescripcion(marca.descripcion);
        setEstado(marca.estado);
        setModalAbierto(true);
    };

    // Abrir el modal para agregar una nueva marca
    const abrirModalAgregar = () => {
        setDescripcion('');
        setEstado(true);
        setEditandoMarca(null);
        setModalAbierto(true);
    };

    useEffect(() => {
        fetchMarcas();
    }, [apiBaseUrl]);

    // Inicializar DataTable
    useEffect(() => {
        if (marcas.length > 0) {
            $('#marcasTable').DataTable({
                pageLength: 10,
                lengthChange: false,
                searching: true,
                ordering: true,
                info: true,
            });
        }
    }, [marcas]);

    return (
        <div className="marcas-container">
            <h2>Listado de Marcas</h2>
            <button onClick={abrirModalAgregar}>
                <i className="fa fa-plus"></i> Agregar Marca
            </button>

            <div className="marcas-table-container">
                <table id="marcasTable" className="display">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Descripcion</th>
                            <th>Estado</th>
                            <th>Acciones</th>
                        </tr>
                    </thead>
                    <tbody>
                        {marcas.map((marca) => (
                            <tr key={marca.id_marca}>
                                <td>{marca.id_marca}</td>
                                <td>{marca.descripcion}</td>
                                <td>{marca.estado ? 'Activo' : 'Inactivo'}</td>
                                <td>
                                    <button onClick={() => handleEditar(marca)}>
                                        <i className="fa fa-edit"></i> Editar
                                    </button>
                                    <button onClick={() => handleEliminar(marca.id_marca)}>
                                        <i className="fa fa-trash"></i> Eliminar
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            {/* Modal para agregar o editar marca */}
            {modalAbierto && (
                <div className="modal">
                    <div className="modal-content">
                        <h3>{editandoMarca ? 'Editar Marca' : 'Agregar Marca'}</h3>
                        <form onSubmit={handleSubmit}>
                            <input
                                type="text"
                                placeholder="Nombre de la marca"
                                value={descripcion}
                                onChange={(e) => setDescripcion(e.target.value)}
                                required
                            />
                            <label>
                                <input
                                    type="checkbox"
                                    checked={estado}
                                    onChange={(e) => setEstado(e.target.checked)}
                                />
                                Activo
                            </label>
                            <button type="submit">{editandoMarca ? 'Guardar Cambios' : 'Agregar'}</button>
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

Marcas.propTypes = {
    apiBaseUrl: PropTypes.string.isRequired,
};

export default Marcas;
