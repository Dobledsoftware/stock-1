import React, { useEffect, useState } from 'react';
import { DataGrid } from '@mui/x-data-grid';
import { Box, Button, Typography, CircularProgress } from '@mui/material';
import Modal from './Modal'; // Componente Modal para editar/inserción de usuarios
import { useSnackbar } from 'notistack';

const Usuarios = () => {
  const { enqueueSnackbar } = useSnackbar();
  const [usuarios, setUsuarios] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedUser, setSelectedUser] = useState(null);
  const [modalOpen, setModalOpen] = useState(false);
  const [accion, setAccion] = useState(''); // 'insert' o 'update'

  // Efecto para obtener usuarios
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

  // Función para editar usuario
  const handleEdit = (usuario) => {
    if (!usuario.id_usuario) return;
    setSelectedUser(usuario);
    setAccion('update');
    setModalOpen(true);
  };

  // Función para resetear contraseña
  const handleResetPassword = async (usuario) => {
    try {
      const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/usuarios`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ accion: 'resetPassword', id_usuario: String(usuario.id_usuario) }),
      });
      const result = await response.json();
      if (result.data.status === 'success') {
        enqueueSnackbar(result.data.message, { variant: 'success' });
      } else {
        enqueueSnackbar('Error al intentar restablecer la contraseña.', { variant: 'error' });
      }
    } catch (error) {
      enqueueSnackbar('Hubo un problema al procesar el reseteo de contraseña.', { variant: 'error' });
    }
  };

  // Abrir modal para agregar nuevo usuario
  const handleAddUser = () => {
    setSelectedUser({ nombre: '', apellido: '', legajo: '', email: '', cuil: '' });
    setAccion('insert');
    setModalOpen(true);
  };

  // Guardar cambios de usuario (insert o update)
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

      // Actualizar el estado según la acción
      if (accion === 'update') {
        setUsuarios((prev) =>
          prev.map((user) =>
            user.id_usuario === updatedUser.id_usuario ? updatedUser : user
          )
        );
      } else {
        setUsuarios((prev) => [...prev, result]);
      }
    } catch (error) {
      enqueueSnackbar('Hubo un problema al procesar el usuario.', { variant: 'error' });
    } finally {
      setModalOpen(false);
    }
  };

  // Definir columnas para el DataGrid
  const columns = [
    {
      field: 'nombreApellido',
      headerName: 'Nombre y Apellido',
      flex: 1,
      valueGetter: (params) => `${params.row.nombre || ''} ${params.row.apellido || ''}`,
    },
    { field: 'legajo', headerName: 'Legajo', flex: 0.5 },
    { field: 'email', headerName: 'Email', flex: 1 },
    { field: 'cuil', headerName: 'CUIL', flex: 0.5 },
    {
      field: 'acciones',
      headerName: 'Acciones',
      flex: 0.7,
      sortable: false,
      renderCell: (params) => (
        <>
          <Button
            variant="contained"
            color="primary"
            size="small"
            onClick={() => handleEdit(params.row)}
            sx={{ mr: 1 }}
          >
            Editar
          </Button>
          <Button
            variant="outlined"
            color="secondary"
            size="small"
            onClick={() => handleResetPassword(params.row)}
          >
            Resetear
          </Button>
        </>
      ),
    },
  ];

  // Preparar las filas para el DataGrid
  const rows = usuarios.map((user) => ({
    id: user.id_usuario,
    ...user,
  }));

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh">
        <CircularProgress />
      </Box>
    );
  }

  if (usuarios.length === 0) {
    return <Typography>No se encontraron usuarios.</Typography>;
  }

  return (
    <Box sx={{ p: 2 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
        <Box
          component="img"
          src="/img/LOGO_POSADAS_sin_fondo_COLOR_HORIZONTAL.png"
          alt="Logo"
          sx={{ height: 50 }}
        />
        <Button variant="contained" color="primary" onClick={handleAddUser}>
          Agregar Usuario
        </Button>
      </Box>
      <Box sx={{ height: 500, width: '100%' }}>
        <DataGrid
          rows={rows}
          columns={columns}
          pageSize={10}
          rowsPerPageOptions={[10, 25, 50]}
          disableSelectionOnClick
        />
      </Box>
      {modalOpen && (
        <Modal
          isOpen={modalOpen}
          onClose={() => setModalOpen(false)}
          user={selectedUser}
          onSave={handleSave}
        />
      )}
    </Box>
  );
};

export default Usuarios;
