import { useEffect, useState } from 'react';
import $ from 'jquery';
import '../../node_modules/datatables.net-dt/css/dataTables.dataTables.css'; // Estilos de DataTables
import 'datatables.net';
import '../styles/Usuarios.css'; // Estilos personalizados de la tabla
import Modal from './Modal'; // Asegúrate de importar el modal

const Usuarios = () => {
  const [usuarios, setUsuarios] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedUser, setSelectedUser] = useState(null);
  const [modalOpen, setModalOpen] = useState(false);

  useEffect(() => {
    const cuil = localStorage.getItem('cuil');

    if (!cuil) {
      alert('No se encontró el CUIL en el localStorage');
      setLoading(false);
      return;
    }

    const fetchUsuarios = async () => {
      try {
        const response = await fetch('http://10.1.16.25:8085/todosLosUsuarios', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ cuil }),
        });

        if (!response.ok) {
          throw new Error('Error en la solicitud');
        }

        const data = await response.json();
        setUsuarios(data);
      } catch (error) {
        console.error('Error:', error);
        alert('Hubo un problema al cargar los usuarios.');
      } finally {
        setLoading(false);
      }
    };

    fetchUsuarios();
  }, []);

  useEffect(() => {
    if (usuarios.length > 0) {
      $(document).ready(() => {
        $('#usuariosTable').DataTable({
          scrollY: '400px',
          scrollCollapse: true,
          paging: true,
          language: {
            decimal: ",",
            thousands: ".",
            lengthMenu: "Mostrar _MENU_ registros por página",
            zeroRecords: "No se encontraron resultados",
            info: "Mostrando página _PAGE_ de _PAGES_",
            infoEmpty: "No hay registros disponibles",
            infoFiltered: "(filtrado de _MAX_ registros en total)",
            search: "Buscar:",
            paginate: {
              first: "Primero",
              last: "Último",
              next: "Siguiente",
              previous: "Anterior",
            },
            loadingRecords: "Cargando...",
            processing: "Procesando...",
            emptyTable: "No hay datos disponibles en la tabla",
            aria: {
              sortAscending: ": activar para ordenar la columna ascendente",
              sortDescending: ": activar para ordenar la columna descendente",
            },
          },
        });
      });
    }
  }, [usuarios]);

  const handleEdit = (usuario) => {
    setSelectedUser(usuario);
    setModalOpen(true);
  };

  const handleSave = async (updatedUser) => {
    const cuil = updatedUser.cuil; // Mantén el CUIL constante

    // Enviar la solicitud de actualización
    try {
      const response = await fetch(`http://10.1.16.25:8085/todosLosUsuariosabm`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ ...updatedUser, cuil }), // Enviar el usuario actualizado
      });

      if (!response.ok) {
        throw new Error('Error en la actualización');
      }

      // Actualizar el estado local
      setUsuarios((prev) =>
        prev.map((user) => (user.cuil === cuil ? updatedUser : user))
      );
    } catch (error) {
      console.error('Error:', error);
      alert('Hubo un problema al actualizar el usuario.');
    }
  };

  const handleAddUser = () => {
    alert('Agregar nuevo usuario');
  };

  if (loading) {
    return <p>Cargando usuarios...</p>;
  }

  if (usuarios.length === 0) {
    return <p>No se encontraron usuarios.</p>;
  }

  return (
    <div className="usuarios-container">
      <h2>Lista de Usuarios</h2>
      <button onClick={handleAddUser} className="btn">
        Agregar Usuario
      </button>
      <table id="usuariosTable" className="display">
        <thead>
          <tr>
            <th>ID Usuario</th>
            <th>Nombre</th>
            <th>Apellido</th>
            <th>Legajo</th>
            <th>Email</th>
            <th>CUIL</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          {usuarios.map((usuario) => (
            <tr key={usuario.id_usuario}>
              <td>{usuario.id_usuario}</td>
              <td>{usuario.nombre}</td>
              <td>{usuario.apellido}</td>
              <td>{usuario.legajo}</td>
              <td>{usuario.email}</td>
              <td>{usuario.cuil}</td>
              <td>
                <button onClick={() => handleEdit(usuario)} className="btn">
                  Editar
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* Aquí agregamos el modal */}
      <Modal
        isOpen={modalOpen}
        onClose={() => setModalOpen(false)}
        user={selectedUser}
        onSave={handleSave}
      />
    </div>
  );
};

export default Usuarios;
