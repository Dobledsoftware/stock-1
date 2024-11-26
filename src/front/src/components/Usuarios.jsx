import { useEffect, useState, useRef } from 'react';
import $ from 'jquery';
import 'datatables.net';
import 'datatables.net-dt/css/dataTables.dataTables.min.css';
import '../styles/Usuarios.css';
import Modal from './Modal'; // Componente del modal
import { useSnackbar } from 'notistack'; // Importar Notistack

const Usuarios = () => {
  const { enqueueSnackbar } = useSnackbar(); // Hook de Notistack para notificaciones
  const [usuarios, setUsuarios] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedUser, setSelectedUser] = useState(null);
  const [modalOpen, setModalOpen] = useState(false);
  const [accion, setAccion] = useState(''); // 'insert' o 'update'
  const tableRef = useRef(null); // Referencia a la tabla

  // Fetch de usuarios
  useEffect(() => {
    const cuil = localStorage.getItem('cuil');
    if (!cuil) {
      alert('No se encontró el CUIL en el localStorage');
      setLoading(false);
      return;
    }

    const fetchUsuarios = async () => {
      try {
        const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/todosLosUsuarios`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ cuil }),
        });

        if (!response.ok) throw new Error('Error en la solicitud');

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

  // Inicialización de DataTables
  useEffect(() => {
    if (usuarios.length > 0 && tableRef.current) {
      const dataTable = $(tableRef.current).DataTable({
        scrollY: '400px',  // Ajusta la altura del scroll según tus necesidades
        scrollCollapse: true,
        paging: true,
        destroy: true,
        responsive: true,  // Hace la tabla adaptable
        language: {
          search: "Buscar:",
          lengthMenu: "Mostrar _MENU_ registros por página",
          zeroRecords: "No se encontraron resultados",
          info: "Mostrando página _PAGE_ de _PAGES_",
          infoEmpty: "No hay registros disponibles",
          infoFiltered: "(filtrado de _MAX_ registros en total)",
          paginate: {
            first: "Primero",
            last: "Último",
            next: "Siguiente",
            previous: "Anterior",
          },
        },
        columnDefs: [
          { width: "40%", targets: 0 },
          { width: "5%", targets: 1 },
          { width: "25%", targets: 2 },
          { width: "15%", targets: 3 },
          { width: "15%", targets: 4 },
        ],
        autoWidth: false,
      });

      // Limpiar el DataTable al desmontar el componente
      return () => {
        dataTable.destroy(true);
      };
    }
  }, [usuarios]);

  // Abrir modal de edición
  const handleEdit = (usuario) => {
    if (!usuario.id_usuario) return;
    setSelectedUser(usuario);
    setAccion('update');
    setModalOpen(true);
  };

  // Función para resetear la contraseña
  const handleResetPassword = async (usuario) => {
    try {
      const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/usuarios`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          accion: 'resetPassword',
          id_usuario: String(usuario.id_usuario), // Convertir a string
        }),
      });
  
      const result = await response.json();
      if (result.data.status === 'success') {
        enqueueSnackbar(result.data.message, { variant: 'success' });
      } else {
        enqueueSnackbar('Error al intentar restablecer la contraseña.', { variant: 'error' });
      }
    // eslint-disable-next-line no-unused-vars
    } catch (error) {
      enqueueSnackbar('Hubo un problema al procesar el reseteo de contraseña.', { variant: 'error' });
    }
  };
  
  // Abrir modal de agregar
  const handleAddUser = () => {
    setSelectedUser({ nombre: '', apellido: '', legajo: '', email: '', cuil: '' });
    setAccion('insert');
    setModalOpen(true);
  };

  // Guardar cambios (insert o update)
  const handleSave = async (updatedUser) => {
    try {
      const payload = { ...updatedUser, accion };
      if (accion === 'update') payload.id_usuario = updatedUser.id_usuario;

      const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/usuarios`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      if (!response.ok) throw new Error('Error en la solicitud');

      const result = await response.json();
      if (result.data.status === 'error') {
        enqueueSnackbar(result.data.message, { variant: 'error' });
        return;
      }

      // Actualiza la lista de usuarios según la acción (insert o update)
      if (accion === 'update') {
        setUsuarios((prev) =>
          prev.map((user) =>
            user.id_usuario === updatedUser.id_usuario ? updatedUser : user
          )
        );
      } else {
        setUsuarios((prev) => [...prev, result]);
      }
    // eslint-disable-next-line no-unused-vars
    } catch (error) {
      enqueueSnackbar('Hubo un problema al procesar el usuario.', { variant: 'error' });
    } finally {
      setModalOpen(false);
    }
  };

  // Mostrar mientras carga o si no hay usuarios
  if (loading) return <h1>Cargando listado de usuarios...</h1>;
  if (usuarios.length === 0) return <p>No se encontraron usuarios.</p>;

  return (
    <div className="usuarios-container">
      <div className="header-container">
        <div className="logo-container">
          <img src="/public/img/LOGO_POSADAS_sin_fondo_COLOR_HORIZONTAL.png" alt="Logo2" className="logo2" />
        </div>
        <button onClick={handleAddUser} className="btn agregar-usuario">Agregar Usuario</button>
      </div>
      <table ref={tableRef} id="usuariosTable" className="display">
        <thead>
          <tr>
            <th>Nombre y Apellido</th>
            <th>Legajo</th>
            <th>Email</th>
            <th>CUIL</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          {usuarios.map((usuario) => (
            <tr key={usuario.id_usuario}>
              <td>{usuario.nombre} {usuario.apellido}</td>
              <td>{usuario.legajo}</td>
              <td>{usuario.email}</td>
              <td>{usuario.cuil}</td>
              <td>
                <button onClick={() => handleEdit(usuario)} className="btn">Editar</button>
                <button onClick={() => handleResetPassword(usuario)} className="btn">Resetear</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* Modal */}
      {modalOpen && (
        <Modal
          isOpen={modalOpen}
          onClose={() => setModalOpen(false)}
          user={selectedUser}
          onSave={handleSave}
        />
      )}
    </div>
  );
};

export default Usuarios;
