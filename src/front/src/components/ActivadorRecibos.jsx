import { useState } from 'react';
import Swal from 'sweetalert2';

const ActivadorRecibos = () => {
  const [recibos, setRecibos] = useState([]);
  const [cuil, setCuil] = useState('');

  // Función para buscar recibos desde el endpoint correcto
  const buscarRecibos = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch('http://10.1.16.25:8085/todos_los_recibos', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ cuil: cuil }) // CUIL enviado para buscar los recibos
      });
      const data = await response.json();

      if (data.length) {
        setRecibos(data); // Llenar la tabla con los recibos obtenidos
      } else {
        Swal.fire('No se encontraron recibos', '', 'info');
      }
    } catch (error) {
      console.error('Error detectado:', error);
    }
  };

  // Función para cambiar el estado del recibo (activar o desactivar)
  const cambiarEstado = async (idRecibo, estadoActual) => {
    const nuevaAccion = estadoActual === 'Activado' ? 'Desactivar' : 'Activar'; // Determina si activar o desactivar

    try {
      const response = await fetch('http://10.1.16.25:8085/recibo', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          accion: nuevaAccion,
          id_recibo: idRecibo
        })
      });

      const result = await response.json();

      if (result.status === 'success') {
        Swal.fire({
          icon: 'success',
          title: result.message,
          showConfirmButton: false,
          timer: 1500
        }).then(() => {
          // Refrescar tabla después de la actualización
          buscarRecibos(new Event('submit')); // Ejecutar la búsqueda nuevamente
        });
      } else {
        Swal.fire({
          icon: 'error',
          title: 'Error',
          text: result.message
        });
      }
    } catch (error) {
      console.error('Error al cambiar estado:', error);
    }
  };

  return (
    <div>
      <form onSubmit={buscarRecibos}>
        <input
          type="text"
          placeholder="Ingrese CUIL"
          value={cuil}
          onChange={(e) => setCuil(e.target.value)}
          required
        />
        <button type="submit">Buscar</button>
      </form>

      <table>
        <thead>
          <tr>
            <th>Id Recibo</th>
            <th>Periodo</th>
            <th>Descripción</th>
            <th>Estado</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          {recibos.map((recibo) => (
            <tr key={recibo.id_recibo}>
              <td>{recibo.id_recibo}</td>
              <td>{recibo.periodo}</td>
              <td>{recibo.descripcion_archivo}</td>
              <td>{recibo.estado}</td>
              <td>
                <button
                  onClick={() => cambiarEstado(recibo.id_recibo, recibo.estado)}
                >
                  {recibo.estado === 'Activado' ? 'Desactivar' : 'Activar'}
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default ActivadorRecibos;
