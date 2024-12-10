import React, { useState } from "react";

const Administracion = () => {
  const [usuarios, setUsuarios] = useState([
    { id: 1, nombre: "Juan Pérez", rol: "Administrador" },
    { id: 2, nombre: "Ana García", rol: "Vendedor" },
    { id: 3, nombre: "Carlos López", rol: "Vendedor" },
  ]);

  const [nuevoUsuario, setNuevoUsuario] = useState({ nombre: "", rol: "Vendedor" });

  const handleAddUser = () => {
    if (nuevoUsuario.nombre.trim() === "") {
      alert("Por favor, ingrese un nombre.");
      return;
    }
    setUsuarios([...usuarios, { id: usuarios.length + 1, nombre: nuevoUsuario.nombre, rol: nuevoUsuario.rol }]);
    setNuevoUsuario({ nombre: "", rol: "Vendedor" });
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>Administración de la Aplicación</h1>

      <div style={{ marginBottom: "20px" }}>
        <h2>Agregar Usuario</h2>
        <div>
          <label htmlFor="nombre">Nombre: </label>
          <input
            type="text"
            id="nombre"
            value={nuevoUsuario.nombre}
            onChange={(e) => setNuevoUsuario({ ...nuevoUsuario, nombre: e.target.value })}
            placeholder="Nombre del usuario"
          />
        </div>
        <div style={{ marginTop: "10px" }}>
          <label htmlFor="rol">Rol: </label>
          <select
            id="rol"
            value={nuevoUsuario.rol}
            onChange={(e) => setNuevoUsuario({ ...nuevoUsuario, rol: e.target.value })}
          >
            <option value="Vendedor">Vendedor</option>
            <option value="Administrador">Administrador</option>
            {/* Agrega más roles según sea necesario */}
          </select>
        </div>
        <button onClick={handleAddUser} style={{ marginTop: "10px" }}>
          Agregar Usuario
        </button>
      </div>

      <div>
        <h2>Lista de Usuarios</h2>
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr>
              <th style={{ border: "1px solid #ddd", padding: "8px" }}>ID</th>
              <th style={{ border: "1px solid #ddd", padding: "8px" }}>Nombre</th>
              <th style={{ border: "1px solid #ddd", padding: "8px" }}>Rol</th>
              <th style={{ border: "1px solid #ddd", padding: "8px" }}>Acciones</th>
            </tr>
          </thead>
          <tbody>
            {usuarios.map((usuario) => (
              <tr key={usuario.id}>
                <td style={{ border: "1px solid #ddd", padding: "8px" }}>{usuario.id}</td>
                <td style={{ border: "1px solid #ddd", padding: "8px" }}>{usuario.nombre}</td>
                <td style={{ border: "1px solid #ddd", padding: "8px" }}>{usuario.rol}</td>
                <td style={{ border: "1px solid #ddd", padding: "8px" }}>
                  <button onClick={() => alert(`Editar usuario ${usuario.id}`)}>Editar</button>
                  <button
                    onClick={() => {
                      setUsuarios(usuarios.filter((u) => u.id !== usuario.id));
                      alert(`Usuario ${usuario.id} eliminado`);
                    }}
                    style={{ marginLeft: "10px" }}
                  >
                    Eliminar
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Administracion;
