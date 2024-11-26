import { useEffect, useState } from 'react';
import $ from 'jquery';
import 'datatables.net';
import '../../node_modules/datatables.net-dt/css/dataTables.dataTables.css'; // Estilos de DataTables
import '../styles/Recibos.css'; // Estilos personalizados de la tabla

const Recibos = () => {
    const recibos = JSON.parse(localStorage.getItem('recibos')) || [];
    const [modalVisible, setModalVisible] = useState(false);
    const [reciboDetalles, setReciboDetalles] = useState('');

    useEffect(() => {
        // Inicializa DataTables después de que la tabla se renderice
        $(document).ready(function () {
            $('#recibosTable').DataTable({
                language: {
                    decimal: ",",
                    thousands: ".",
                    lengthMenu: "_MENU_Registros por página",
                    zeroRecords: "No se enontraron resultados",
                    info: "Página _PAGE_ de _PAGES_",
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
    }, []);

    const verDetalles = (idRecibo) => {
        // Aquí puedes obtener los detalles del recibo
        // Simularemos que obtenemos detalles de la API
        const detalles = `Detalles del recibo ID: ${idRecibo}`; // Actualiza con la información real
        setReciboDetalles(detalles);
        setModalVisible(true);
    };

    const descargarRecibo = (idRecibo) => {
        // Lógica para descargar recibo
        alert(`Descargar recibo ID: ${idRecibo}`);
    };

    const closeModal = () => {
        setModalVisible(false);
    };

    return (
        <div className="recibos-container">
            <table id="recibosTable" className="display">
                <thead>
                    <tr>
                        <th>Periodo</th>
                        <th>Recibo</th>
                        <th>Acciones</th>
                    </tr>
                </thead>
                <tbody>
                    {recibos.map((recibo) => (
                        <tr key={recibo.id_recibo}>
                            <td>{recibo.periodo}</td>
                            <td>{recibo.descripcion_archivo}</td>
                            <td>
                                <button onClick={() => verDetalles(recibo.id_recibo)} className="btn-detalles">
                                    Ver Detalles
                                </button>
                                <button onClick={() => descargarRecibo(recibo.id_recibo)} className="btn-detalles">
                                    Descargar
                                </button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>

            {/* Modal para ver detalles */}
            {modalVisible && (
                <div className="modal">
                    <div className="modal-content">
                        <span className="close" onClick={closeModal}>&times;</span>
                        <h2>Detalles del Recibo</h2>
                        <p>{reciboDetalles}</p>
                        {/* Puedes agregar más detalles aquí */}
                    </div>
                </div>
            )}
        </div>
    );
};

export default Recibos;
