import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import '../styles/categorias.css'; // Importamos los estilos específicos para este componente
import $ from 'jquery'; // Necesario para DataTables
import Swal from 'sweetalert2'; // Importar SweetAlert

const Categorias = ({ apiBaseUrl }) => {
    const [categorias, setCategorias] = useState([]);
    const [descripcion, setDescripcion] = useState('');
    const [estado, setEstado] = useState(true);
    const [editandoCategoria, setEditandoCategoria] = useState(null);
    const [modalAbierto, setModalAbierto] = useState(false); // Estado para controlar la visibilidad del modal

    // Fetch inicial para listar categorías
    const fetchCategorias = async (incluirInactivas = true) => {
        try {
            const response = await fetch(
                `${import.meta.env.VITE_API_BASE_URL}/productos_categorias?estado=true`,
                {
                  method: "GET",
                  headers: {
                    "Content-Type": "application/json",
                  },
                }
              );

            if (response.ok) {
                const { data } = await response.json();
                setCategorias(data); // Se actualiza el estado con los datos recibidos
            } else {
                throw new Error('Error al listar categorías.');
            }
        } catch (err) {
            console.error(err.message);
        }
    };

    // Crear o editar categoría
    const handleSubmit = async (e) => {
        e.preventDefault();
        const accion = editandoCategoria ? 'modificarCategoria' : 'agregarCategoria';
        const body = editandoCategoria
            ? {
                  accion,
                  id_categoria: editandoCategoria.id_categoria,
                  descripcion,
                  estado,
              }
            : {
                  accion,
                  descripcion,
                  estado,
              };

        try {
            const response = await fetch(`${apiBaseUrl}/producto_categoria`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(body),
            });

            if (response.ok) {
                Swal.fire({
                    icon: 'success',
                    title: `Categoría ${editandoCategoria ? 'modificada' : 'agregada'} con éxito`,
                    showConfirmButton: false,
                    timer: 1500,
                });
                setDescripcion('');
                setEstado(true);
                setEditandoCategoria(null);
                setModalAbierto(false);
                fetchCategorias(); // Actualizar la lista de categorías
            } else {
                throw new Error('Error al guardar la categoría.');
            }
        } catch (err) {
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: err.message,
            });
        }
    };

    // Eliminar categoría (soft delete)
    const handleEliminar = async (idCategoria) => {
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
                    const response = await fetch(`${apiBaseUrl}/producto_categoria`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            accion: 'eliminarCategoria',
                            id_categoria: idCategoria,
                        }),
                    });

                    if (response.ok) {
                        Swal.fire({
                            icon: 'success',
                            title: 'Categoría eliminada con éxito',
                            showConfirmButton: false,
                            timer: 1500,
                        });
                        fetchCategorias();
                    } else {
                        throw new Error('Error al eliminar la categoría.');
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

    // Seleccionar una categoría para edición
    const handleEditar = (categoria) => {
        setEditandoCategoria(categoria);
        setDescripcion(categoria.descripcion);
        setEstado(categoria.estado);
        setModalAbierto(true);
    };

    // Abrir el modal para agregar una nueva categoría
    const abrirModalAgregar = () => {
        setDescripcion('');
        setEstado(true);
        setEditandoCategoria(null);
        setModalAbierto(true);
    };

    useEffect(() => {
        fetchCategorias();
    }, [apiBaseUrl]);

    // Inicializar DataTable
    useEffect(() => {
        if (categorias.length > 0) {
            $('#categoriasTable').DataTable({
                pageLength: 10, // Establecer el límite de 10 registros por página
                lengthChange: false, // Desactivar el selector de cantidad de registros por página
                searching: true, // Activar la búsqueda
                ordering: true, // Permitir ordenar las columnas
                info: true, // Mostrar la información de cuántos registros hay
            });
        }
    }, [categorias]);

    return (
        <div className="categorias-container">
            <h2>Listado de Categorías</h2>
            <button onClick={abrirModalAgregar}>
                <i className="fa fa-plus"></i> Agregar Categoría
            </button>

            <div className="categorias-table-container">
                <table id="categoriasTable" className="display">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Descripción</th>
                            <th>Estado</th>
                            <th>Acciones</th>
                        </tr>
                    </thead>
                    <tbody>
                        {categorias.map((categoria) => (
                            <tr key={categoria.id_categoria}>
                                <td>{categoria.id_categoria}</td>
                                <td>{categoria.descripcion}</td>
                                <td>{categoria.estado ? 'Activo' : 'Inactivo'}</td>
                                <td>
                                    <button onClick={() => handleEditar(categoria)}>
                                        <i className="fa fa-pencil"></i> Editar
                                    </button>
                                    <button onClick={() => handleEliminar(categoria.id_categoria)}>
                                        <i className="fa fa-trash"></i> Eliminar
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            {/* Modal para agregar o editar categoría */}
            {modalAbierto && (
                <div className="modal">
                    <div className="modal-content">
                        <h3>{editandoCategoria ? 'Editar Categoría' : 'Agregar Categoría'}</h3>
                        <form onSubmit={handleSubmit}>
                            <input
                                type="text"
                                placeholder="Descripción de la categoría"
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
                            <button type="submit">{editandoCategoria ? 'Guardar Cambios' : 'Agregar'}</button>
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

Categorias.propTypes = {
    apiBaseUrl: PropTypes.string.isRequired,
};

export default Categorias;
