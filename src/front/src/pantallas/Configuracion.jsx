import React, { useState, useEffect } from "react";
import axios from "axios";

const API_BASE_URL = "http://92.112.176.191:8085";

const GestionPerfiles = () => {
  const [perfiles, setPerfiles] = useState([]);
  const [usuarios, setUsuarios] = useState([]);
  const [usuariosPerfil, setUsuariosPerfil] = useState([]);
  const [funciones, setFunciones] = useState([]);
  const [funcionesPerfil, setFuncionesPerfil] = useState([]);
  const [selectedPerfil, setSelectedPerfil] = useState(null);
  const [selectedUsuario, setSelectedUsuario] = useState(null);
  const [modalType, setModalType] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchPerfiles();
    fetchUsuarios();
    fetchFunciones();
  }, []);

  const fetchPerfiles = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/perfiles?estado=true`);
      setPerfiles(response.data.perfiles || []);
    } catch (error) {
      console.error("Error al obtener perfiles", error);
    }
  };

  const fetchUsuarios = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/usuarios?estado=true`);
      console.log("Respuesta completa de la API:", response.data); // Debugging
      setUsuarios(Array.isArray(response.data) ? response.data : []);
    } catch (error) {
      console.error("Error al obtener usuarios", error);
    }
  };

  const fetchUsuariosPerfil = async (id_perfil) => {
    setLoading(true);
    try {
      const response = await axios.get(`${API_BASE_URL}/perfiles/${id_perfil}/usuarios`);
      setUsuariosPerfil(response.data.usuarios || []);
    } catch (error) {
      console.error("Error al obtener usuarios del perfil", error);
    }
    setLoading(false);
  };

  const openAssignUsuarioModal = (perfil) => {
    console.log("Perfil seleccionado antes de asignar:", perfil); // Debugging
    setSelectedPerfil(perfil);
  
    setTimeout(() => {
      console.log("Perfil seleccionado después de asignar:", selectedPerfil); // Debugging
      fetchUsuarios(); // Asegura que la lista de usuarios se obtiene antes de abrir el modal
      setModalType("assignUsuario");
    }, 100); // Espera breve para permitir la actualización del estado
  };
 
  const handleAssignUsuario = async () => {
    if (!selectedPerfil || !selectedUsuario) return;
    try {
      console.log(`Asignando usuario ${selectedUsuario} al perfil ${selectedPerfil.id_perfil}`);
      const response = await axios.post(`${API_BASE_URL}/perfiles/${selectedPerfil.id_perfil}/usuarios/${selectedUsuario}`);
      if (response.status === 201) {
        console.log("✅ Usuario asignado correctamente");
      } else if (response.status === 403) {
        console.error("🚫 El usuario no está activo");
      } else if (response.status === 404) {
        console.error("🔍 Usuario o perfil no encontrados");
      } else if (response.status === 409) {
        console.error("⚠️ El usuario ya tiene un perfil asignado");
      } else if (response.status === 500) {
        console.error("❌ Error interno del servidor");
      }
      fetchUsuariosPerfil(selectedPerfil.id_perfil);
      setModalType(null);
    } catch (error) {
      console.error("Error al asignar usuario", error);
    }
  };

  
  
  const fetchFunciones = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/funciones`);
      setFunciones(response.data.funciones || []);
    } catch (error) {
      console.error("Error al obtener funciones", error);
    }
  };

  const fetchFuncionesPerfil = async (id_perfil) => {
    setLoading(true);
    try {
      const response = await axios.get(`${API_BASE_URL}/perfiles/${id_perfil}/funciones`);
      setFuncionesPerfil(response.data.funciones || []);
    } catch (error) {
      console.error("Error al obtener funciones del perfil", error);
    }
    setLoading(false);
  };

  const handleViewUsuarios = (perfil) => {
    setSelectedPerfil(perfil);
    fetchUsuariosPerfil(perfil.id_perfil);
    setModalType("viewUsuarios");
  };

  const handleViewFunciones = (perfil) => {
    setSelectedPerfil(perfil);
    fetchFuncionesPerfil(perfil.id_perfil);
    setModalType("viewFunciones");
  };

  const handleCloseModal = () => {
    setModalType(null);
  };

  return (
    <div>
      <h2>Gestión de Perfiles</h2>
      <table border="1" cellPadding="5" cellSpacing="0">
        <thead>
          <tr>
            <th>ID</th>
            <th>Nombre</th>
            <th>Descripción</th>
            <th>Estado</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          {perfiles.map((perfil) => (
            <tr key={perfil.id_perfil}>
              <td>{perfil.id_perfil}</td>
              <td>{perfil.nombre}</td>
              <td>{perfil.descripcion}</td>
              <td>{perfil.estado ? "Activo" : "Inactivo"}</td>
              <td>
                <button onClick={() => handleViewUsuarios(perfil)}>Ver Usuarios</button>
                <button onClick={() => openAssignUsuarioModal(perfil)}>Asignar Usuario</button>
                <button onClick={() => handleViewFunciones(perfil)}>Ver Funciones</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {modalType === "assignUsuario" && (
        <div>
          <h3>Asignar Usuario al Perfil</h3>
          <select onChange={(e) => setSelectedUsuario(e.target.value)}>
                 <option value="">Seleccione un usuario</option>
                {console.log("Lista de usuarios dentro del select:", usuarios)} {/* Debugging */}
                {Array.isArray(usuarios) && usuarios.length > 0 ? (
                  usuarios.map((usuario) => (
                    <option key={usuario.id_usuario} value={usuario.id_usuario}>
                      {usuario.nombre} {usuario.apellido} ({usuario.email})
                    </option>
                  ))
                ) : (
                 <option value="">No hay usuarios disponibles</option>
              )}
          </select>

          <button onClick={handleAssignUsuario}>Asignar</button>
          <button onClick={handleCloseModal}>Cerrar</button>
        </div>
      )}

      {modalType === "viewUsuarios" && (
        <div>
          <h3>Usuarios del Perfil</h3>
          {loading ? <p>Cargando...</p> : (
            <table border="1" cellPadding="5" cellSpacing="0">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Nombre</th>
                </tr>
              </thead>
              <tbody>
                {usuariosPerfil.length > 0 ? (
                  usuariosPerfil.map((usuario) => (
                    <tr key={usuario.id_usuario}>
                      <td>{usuario.id_usuario}</td>
                      <td>{usuario.nombre}</td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan="2">No hay usuarios asignados</td>
                  </tr>
                )}
              </tbody>
            </table>
          )}
          <button onClick={handleCloseModal}>Cerrar</button>
        </div>
      )}

      {modalType === "viewFunciones" && (
        <div>
          <h3>Funciones del Perfil</h3>
          {loading ? <p>Cargando...</p> : (
            <table border="1" cellPadding="5" cellSpacing="0">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Nombre</th>
                </tr>
              </thead>
              <tbody>
                {funcionesPerfil.length > 0 ? (
                  funcionesPerfil.map((funcion) => (
                    <tr key={funcion.id_funcion}>
                      <td>{funcion.id_funcion}</td>
                      <td>{funcion.nombre}</td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan="2">No hay funciones asignadas</td>
                  </tr>
                )}
              </tbody>
            </table>
          )}
          <button onClick={handleCloseModal}>Cerrar</button>
        </div>
      )}
    </div>
  );
};

export default GestionPerfiles;
