import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import Swal from 'sweetalert2';

const Estantes = ({ apiBaseUrl, id_almacen, estado }) => {
    const [estantes, setEstantes] = useState([]);
    const [descripcion, setDescripcion] = useState('');
    const [editandoEstantes, setEditandoEstantes] = useState(null);

    // Fetch inicial para listar estantes del almacén con estado
    const fetchEstantes = async () => {
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
                setEstantes(data);
            } else {
                throw new Error('Error al listar Estantes.');
            }
        } catch (err) {
            console.error(err.message);
        }
    };

    useEffect(() => {
        fetchEstantes();
    }, [id_almacen, estado]); // Se asegura de actualizar si cambia el estado o el id_almacen

    // Lógica para agregar/editar estante
    const handleSubmit = async (e) => {
        e.preventDefault();
        const accion = editandoEstantes ? 'editarEstante' : 'agregarEstante';
        const body = editandoEstantes
            ? {
                  accion,
                  id_estante: editandoEstantes.id_estante,
                  descripcion,
                  id_almacen, // Asegúrate de enviar el id_almacen
              }
            : {
                  accion,
                  descripcion,
                  id_almacen, // Asegúrate de enviar el id_almacen
              };

        try {
            const response = await fetch(`${apiBaseUrl}/almacen_estante`, {
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
                setEditandoEstantes(null);
                fetchEstantes(); // Recargar los estantes
            } else {
                throw new Error('Error al guardar el Estante.');
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
        <div>
            <h3>Estantes de Almacén {id_almacen}</h3>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    placeholder="Descripción del Estante"
                    value={descripcion}
                    onChange={(e) => setDescripcion(e.target.value)}
                    required
                />
                <button type="submit">{editandoEstantes ? 'Guardar Cambios' : 'Agregar Estante'}</button>
            </form>

            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Descripción</th>
                        <th>Acciones</th>
                    </tr>
                </thead>
                <tbody>
                    {estantes.map((estante) => (
                        <tr key={estante.id_estante}>
                            <td>{estante.id_estante}</td>
                            <td>{estante.descripcion}</td>
                            <td>
                                <button onClick={() => setEditandoEstantes(estante)}>
                                    Editar
                                </button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

Estantes.propTypes = {
    apiBaseUrl: PropTypes.string.isRequired,
    id_almacen: PropTypes.number.isRequired,
    estado: PropTypes.bool.isRequired,  // Asegurarse de que el estado es obligatorio
};

export default Estantes;
