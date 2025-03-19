import { useEffect, useState } from "react";
import axios from "axios";
import {
  Button,
  Table,
  TableHead,
  TableBody,
  TableRow,
  TableCell,
  TextField,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
} from "@mui/material";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export default function Administracion() {
  const [usuarios, setUsuarios] = useState([]);
  const [loading, setLoading] = useState(true);
  const [modal, setModal] = useState(false);
  const [selectedUser, setSelectedUser] = useState(null);
  const [editedUser, setEditedUser] = useState({});
  const [nuevoUsuario, setNuevoUsuario] = useState({ nombre: "", apellido: "", email: "", usuario: "", password: "" });
  const [modalNuevo, setModalNuevo] = useState(false);

  useEffect(() => {
    fetchUsuarios();
  }, []);

  const fetchUsuarios = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/usuarios?estado=true`);
      setUsuarios(response.data);
    } catch (error) {
      console.error("Error al obtener usuarios", error);
    } finally {
      setLoading(false);
    }
  };

  const handleEdit = (usuario) => {
    setSelectedUser(usuario);
    setEditedUser(usuario);
    setModal(true);
  };

  const handleInactivate = async (id_usuario) => {
    if (window.confirm("¿Estás seguro de que deseas inactivar este usuario?")) {
      try {
        await axios.put(`${API_BASE_URL}/usuarios/${id_usuario}/estado?estado=false`);
        fetchUsuarios();
        alert("Usuario inactivado exitosamente");
      } catch (error) {
        console.error("Error al inactivar usuario", error);
      }
    }
  };

  const handleSave = async () => {
    if (window.confirm("¿Confirmas los cambios en este usuario?")) {
      try {
        await axios.put(`${API_BASE_URL}/usuarios/${selectedUser.id_usuario}`, editedUser);
        setModal(false);
        fetchUsuarios();
        alert("Usuario actualizado exitosamente");
      } catch (error) {
        console.error("Error al actualizar usuario", error);
      }
    }
  };

  // ABRIR MODAL PARA CREAR USUARIO
  const handleOpenNewUserModal = () => {
    setNuevoUsuario({ nombre: "", apellido: "", email: "", usuario: "", password: "" });
    setModalNuevo(true);
  };

  // GUARDAR NUEVO USUARIO
  const handleCreateUser = async () => {
    // Validar que los campos requeridos estén completos antes de enviar la solicitud
    if (!nuevoUsuario.nombre || !nuevoUsuario.apellido || !nuevoUsuario.email || !nuevoUsuario.usuario || !nuevoUsuario.password) {
      alert("Todos los campos son obligatorios.");
      return;
    }
  
    try {
      const payload = {
        nombre: nuevoUsuario.nombre.trim(),
        apellido: nuevoUsuario.apellido.trim(),
        email: nuevoUsuario.email.trim(),
        usuario: nuevoUsuario.usuario.trim(),
        password: nuevoUsuario.password, // No aplicar trim() en contraseñas
      };
  
      const response = await axios.post(`${API_BASE_URL}/usuarios`, payload, {
        headers: {
          "Content-Type": "application/json", // Asegura que los datos se envíen como JSON
        },
      });
  
      if (response.status === 201) {
        alert("Usuario agregado correctamente");
        fetchUsuarios();
        setModalNuevo(false);
      }
    } catch (error) {
      if (error.response?.status === 409) {
        alert("El email o usuario ya está en uso.");
      } else {
        console.error("Error al crear usuario", error);
      }
    }
  };
  
  return (
    <div>
      <h1 className="text-xl font-bold mb-4">Administración de la Aplicación</h1>

      {/* Botón para agregar un nuevo usuario */}
      <Button variant="contained" color="primary" onClick={handleOpenNewUserModal} style={{ marginBottom: "20px" }}>
        Agregar Usuario
      </Button>

      <h2 className="mt-4">Lista de Usuarios</h2>
      {loading ? (
        <p>Cargando...</p>
      ) : (
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>ID</TableCell>
              <TableCell>Nombre</TableCell>
              <TableCell>Apellido</TableCell>
              <TableCell>Email</TableCell>
              <TableCell>Usuario</TableCell>
              <TableCell>Acciones</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {usuarios.map((usuario) => (
              <TableRow key={usuario.id_usuario}>
                <TableCell>{usuario.id_usuario}</TableCell>
                <TableCell>{usuario.nombre}</TableCell>
                <TableCell>{usuario.apellido}</TableCell>
                <TableCell>{usuario.email}</TableCell>
                <TableCell>{usuario.usuario}</TableCell>
                <TableCell>
                  <Button onClick={() => handleEdit(usuario)}>Editar</Button>
                  <Button onClick={() => handleInactivate(usuario.id_usuario)} color="error">Inactivar</Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      )}

      {/* Modal para editar usuario */}
      <Dialog open={modal} onClose={() => setModal(false)}>
        <DialogTitle>Editar Usuario</DialogTitle>
        <DialogContent>
          <TextField label="Nombre" value={editedUser.nombre} onChange={(e) => setEditedUser({ ...editedUser, nombre: e.target.value })} fullWidth margin="normal" />
          <TextField label="Apellido" value={editedUser.apellido} onChange={(e) => setEditedUser({ ...editedUser, apellido: e.target.value })} fullWidth margin="normal" />
          <TextField label="Email" value={editedUser.email} onChange={(e) => setEditedUser({ ...editedUser, email: e.target.value })} fullWidth margin="normal" />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setModal(false)}>Cancelar</Button>
          <Button onClick={handleSave} color="primary">Guardar</Button>
        </DialogActions>
      </Dialog>

      {/* Modal para agregar nuevo usuario */}
      <Dialog open={modalNuevo} onClose={() => setModalNuevo(false)}>
        <DialogTitle>Agregar Nuevo Usuario</DialogTitle>
        <DialogContent>
          <TextField label="Nombre" value={nuevoUsuario.nombre} onChange={(e) => setNuevoUsuario({ ...nuevoUsuario, nombre: e.target.value })} fullWidth margin="normal" />
          <TextField label="Apellido" value={nuevoUsuario.apellido} onChange={(e) => setNuevoUsuario({ ...nuevoUsuario, apellido: e.target.value })} fullWidth margin="normal" />
          <TextField label="Email" value={nuevoUsuario.email} onChange={(e) => setNuevoUsuario({ ...nuevoUsuario, email: e.target.value })} fullWidth margin="normal" />
          <TextField label="Usuario" value={nuevoUsuario.usuario} onChange={(e) => setNuevoUsuario({ ...nuevoUsuario, usuario: e.target.value })} fullWidth margin="normal" />
          <TextField label="Contraseña" type="password" value={nuevoUsuario.password} onChange={(e) => setNuevoUsuario({ ...nuevoUsuario, password: e.target.value })} fullWidth margin="normal" />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setModalNuevo(false)}>Cancelar</Button>
          <Button onClick={handleCreateUser} color="primary">Crear</Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}
