import React from 'react';
import PropTypes from 'prop-types';
import '../styles/Modal.css'; // Asegúrate de crear este archivo CSS

const Modal = ({ isOpen, onClose, user, onSave }) => {
  // Estado del formulario
  const [formData, setFormData] = React.useState({ ...user });

  // Actualiza el estado cuando cambia el usuario
  React.useEffect(() => {
    setFormData({ ...user });
  }, [user]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    // Crear el objeto JSON según la acción (insert o update)
    const jsonToSend = {
      accion: user?.id_usuario ? "update" : "insert", // Cambia la acción según el caso
      id_usuario: user?.id_usuario ? String(user.id_usuario) : null, // Convertir id_usuario a string si existe
      cuil: formData.cuil || "", // Asegúrate de que 'cuil' esté en el estado
      nombre: formData.nombre || "",
      apellido: formData.apellido || "",
      legajo: formData.legajo || "",
      email: formData.email || ""
    };

    console.log("Enviando JSON:", jsonToSend); // Mostrar el JSON en la consola

    // Llamar a la función onSave con el JSON que has creado
    onSave(jsonToSend);
    onClose();
  };

  // Mover la evaluación condicional después de llamar los hooks
  if (!isOpen) return null;

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <h2>{user?.id_usuario ? 'Editar Usuario' : 'Agregar Usuario'}</h2>
        <form onSubmit={handleSubmit}>
          <label>
            CUIL:
            <input
              type="text"
              name="cuil"
              value={formData.cuil || ''}
              onChange={handleChange}
              required
            />
          </label>
          <label>
            Nombre:
            <input
              type="text"
              name="nombre"
              value={formData.nombre || ''}
              onChange={handleChange}
              required
            />
          </label>
          <label>
            Apellido:
            <input
              type="text"
              name="apellido"
              value={formData.apellido || ''}
              onChange={handleChange}
              required
            />
          </label>
          <label>
            Legajo:
            <input
              type="text"
              name="legajo"
              value={formData.legajo || ''}
              onChange={handleChange}
              required
            />
          </label>
          <label>
            Email:
            <input
              type="email"
              name="email"
              value={formData.email || ''}
              onChange={handleChange}
              required
            />
          </label>
          <div className="modal-buttons">
            <button type="submit" className="btn guardar">Guardar</button>
            <button type="button" className="btn cancelar" onClick={onClose}>Cancelar</button>
          </div>
        </form>
      </div>
    </div>
  );
};

// Define PropTypes para la validación de props
Modal.propTypes = {
  isOpen: PropTypes.bool.isRequired, // isOpen debe ser un booleano requerido
  onClose: PropTypes.func.isRequired, // onClose debe ser una función requerida
  onSave: PropTypes.func.isRequired, // onSave debe ser una función requerida
  user: PropTypes.shape({
    id_usuario: PropTypes.number, // id_usuario es un número (puede ser opcional si estás agregando)
    cuil: PropTypes.string, // CUIL debe ser un string
    nombre: PropTypes.string, // nombre debe ser un string
    apellido: PropTypes.string, // apellido debe ser un string
    legajo: PropTypes.string, // legajo debe ser un string
    email: PropTypes.string, // email debe ser un string
  }).isRequired, // user debe ser un objeto con las propiedades anteriores, y es requerido
};

export default Modal;
