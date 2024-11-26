import { useState} from 'react';
import Swal from 'sweetalert2';
import DataTable from 'react-data-table-component';
import '../styles/Activador.css'; // Estilos personalizados de la tabla

const RecibosTable = () => {
  const [recibos, setRecibos] = useState([]);
  const [cuil, setCuil] = useState('');

  // Función para cargar recibos desde la API
  const cargarRecibos = async () => {
    try {
      const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/todos_los_recibos`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ cuil }),
      });

      const data = await response.json();
      if (data.length > 0) {
        setRecibos(data);
      } else {
        Swal.fire('No se encontraron recibos', '', 'info');
      }
    } catch (error) {
      console.error('Error al cargar los recibos:', error);
    }
  };

  // Función para cambiar el estado (activar/desactivar) de un recibo
  const cambiarEstadoRecibo = async (idRecibo, nuevaAccion) => {
    const jsonToSend = {
      accion: nuevaAccion,
      id_recibo: `${idRecibo}`, // Id con comillas como string
    };

    console.log('Enviando JSON al endpoint:', jsonToSend);

    try {
      const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/recibo`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(jsonToSend),
      });

      const result = await response.json();
      if (result.status === 'success') {
        Swal.fire({
          icon: 'success',
          title: result.message,
          showConfirmButton: false,
          timer: 1500,
          heightAuto: false, // Evita que el body cambie de tamaño
        }).then(() => {
          cargarRecibos(); // Refrescar la tabla
        });
      } else {
        Swal.fire({
          icon: 'error',
          title: 'Error',
          text: result.message,
        });
      }
    } catch (error) {
      console.error('Error al cambiar estado:', error);
    }
  };

  // Manejador del formulario para buscar recibos por CUIL
  const handleSubmit = (e) => {
    e.preventDefault();
    cargarRecibos();
  };

  // Definimos las columnas del DataTable
  const columns = [
    {
      name: 'Periodo',
      selector: (row) => row.periodo,
      sortable: true,
    },
    {
      name: 'Descripción',
      selector: (row) => row.descripcion_archivo,
      sortable: true,
    },
    {
      name: 'Estado',
      selector: (row) => row.estado,
      sortable: true,
    },
    {
      name: 'Acciones',
      cell: (row) => (
        <button
          onClick={() =>
            cambiarEstadoRecibo(
              row.id_recibo,
              row.estado === 'Activado' ? 'Desactivado' : 'Activado'
            )
          }
        >
          {row.estado === 'Activado' ? 'Desactivar' : 'Activar'}
        </button>
      ),
    },
  ];

  return (
    <div>
     

 <div className="recibos-container">
  {/* Logo de la aplicación */}
  <div className="logo-container">
                <img src="/public/img/LOGO_POSADAS_sin_fondo_COLOR_HORIZONTAL.png" alt="Logo2" className="logo2"/>
            </div>
 <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={cuil}
          onChange={(e) => setCuil(e.target.value)}
          placeholder="Ingrese CUIL"
          required
        />
        <button type="submit" className="btn">Buscar</button>
      </form>
      <h2>Lista de Recibos</h2>
      <DataTable
        title="Recibos"
        columns={columns}
        data={recibos}
        pagination
        highlightOnHover
        noDataComponent="No hay registros para mostrar"  // Mensaje en español
        className="display"
        customStyles={{
          rows: {
            style: {
              minHeight: '72px', // override the row height
            },
          },
          headCells: {
            style: {
              backgroundColor: '#04117e',
              color: 'white',
              fontWeight: 'bold',
              textAlign: 'left',
            },
          },
          cells: {
            style: {
              padding: '12px 15px',
              overflow: 'hidden',
              textOverflow: 'ellipsis',
              whiteSpace: 'nowrap',
            },
          },
        }}
      />   </div>
    </div>
  );
};

export default RecibosTable;
