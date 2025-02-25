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
  Select,
  MenuItem
} from "@mui/material";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export default function Administracion() {
  const [usuarios, setUsuarios] = useState([]);
  const [loading, setLoading] = useState(true);
  const [modal, setModal] = useState(false);
  const [selectedUser, setSelectedUser] = useState(null);
  const [editedUser, setEditedUser] = useState({});
  const [nuevoUsuario, setNuevoUsuario] = useState({ nombre: "", apellido: "", email: "", usuario: "", rol: "Vendedor" });

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

  return (
    <div>
      <h1 className="text-xl font-bold mb-4">Administración de la Aplicación</h1>
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
              <TableCell>Rol</TableCell>
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
                <TableCell>{usuario.rol}</TableCell>
                <TableCell>
                  <Button onClick={() => handleEdit(usuario)}>Editar</Button>
                  <Button onClick={() => handleInactivate(usuario.id_usuario)} color="error">Inactivar</Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      )}
      <Dialog open={modal} onClose={() => setModal(false)}>
        <DialogTitle>Editar Usuario</DialogTitle>
        <DialogContent>
          <TextField
            label="Nombre"
            value={editedUser.nombre}
            onChange={(e) => setEditedUser({ ...editedUser, nombre: e.target.value })}
            fullWidth
            margin="normal"
          />
          <TextField
            label="Apellido"
            value={editedUser.apellido}
            onChange={(e) => setEditedUser({ ...editedUser, apellido: e.target.value })}
            fullWidth
            margin="normal"
          />
          <TextField
            label="Email"
            value={editedUser.email}
            onChange={(e) => setEditedUser({ ...editedUser, email: e.target.value })}
            fullWidth
            margin="normal"
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setModal(false)}>Cancelar</Button>
          <Button onClick={handleSave} color="primary">Guardar</Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}
