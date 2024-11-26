import { useEffect, useState } from 'react';
import $ from 'jquery';
import 'datatables.net';
import '../../node_modules/datatables.net-dt/css/dataTables.dataTables.css';
import '../styles/Recibos.css';

const Recibos = () => {
    const recibos = JSON.parse(localStorage.getItem('recibos')) || [];
    const [modalVisible, setModalVisible] = useState(false);
    const [pdfUrl, setPdfUrl] = useState('');
    const [loadingRecibo, setLoadingRecibo] = useState({});
    const [showCredencial, setShowCredencial] = useState(false);

    const nombre = localStorage.getItem('nombre');
    const apellido = localStorage.getItem('apellido');
    const cuil = localStorage.getItem('cuil'); 
    const legajo = localStorage.getItem('legajo'); 
    const email = localStorage.getItem('email');

        useEffect(() => {
            const table = $('#recibosTable').DataTable({
                destroy: true,
                language: {
                    decimal: ",",
                    thousands: ".",
                    lengthMenu: "_MENU_ Registros por página",
                    zeroRecords: "No se encontraron resultados",
                    info: "Página _PAGE_ de _PAGES_",
                    infoEmpty: "No hay registros disponibles",
                    infoFiltered: "(filtrado de _MAX_ registros en total)",
                    search: "",
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
                initComplete: function () {
                    // Aquí puedes aplicar estilos adicionales
                    $('.display').css({
                        'width': '100%',
                        'border-collapse': 'collapse',
                        'margin': '20px auto',
                        'font-size': '18px',
                        'text-align': 'left',
                        'background-color': 'white',
                        'table-layout': 'fixed',
                    });
        
                    // Asegúrate de que los estilos de los encabezados y celdas se aplican
                    $('.display th').css({
                        'background-color': '#0983e7',
                        'color': 'white',
                        'font-weight': 'bold',
                        'padding': '12px 15px'
                    });
        
                    $('.display td').css({
                        'padding': '12px 15px',
                        'overflow': 'hidden',
                        'text-overflow': 'ellipsis',
                        'white-space': 'nowrap'
                    });
                }
            });
        
            return () => {
                table.destroy();
            };
        }, []);
        

    const verDetalles = async (idRecibo) => {
        setLoadingRecibo((prev) => ({ ...prev, [idRecibo]: true }));
        try {
            const response = await fetch('${import.meta.env.VITE_API_BASE_URL}/download', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ id_recibo: String(idRecibo) }),
            });

            if (!response.ok) {
                throw new Error(`Error al obtener el recibo: ${response.statusText}`);
            }

            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            setPdfUrl(url);
            setModalVisible(true);
        } catch (error) {
            console.error('Error al obtener el recibo:', error);
            alert(`Hubo un error al visualizar el recibo. Mensaje: ${error.message}. Inténtalo de nuevo.`);
        } finally {
            setLoadingRecibo((prev) => ({ ...prev, [idRecibo]: false }));
        }
    };

    const closeModal = () => {
        setModalVisible(false);
        setPdfUrl('');
    };

    return (
        <div className="recibos-container">
            <div className="logo-container">
                <img src="/public/img/LOGO_POSADAS_sin_fondo_COLOR_HORIZONTAL.png" alt="Logo2" className="logo2"/>
            </div>

            <button className="btn-detalles" onClick={() => setShowCredencial(!showCredencial)}>
                {showCredencial ? 'Ocultar Datos' : 'Mis Datos'}
            </button>

            {showCredencial && (
                <div className="credencial-container">
                    <div className="credencial">
                        <div className="credencial-body">
                            <p><strong>Nombre y Apellido:</strong> {nombre} {apellido}</p>
                            <p><strong>CUIL:</strong> {cuil}</p>
                            <p><strong>Legajo:</strong> {legajo}</p>
                            <p><strong>Email:</strong> {email}</p>
                        </div>
                    </div>
                </div>
            )}

            <div className="tabla-container">
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
                                    <button
                                        onClick={() => verDetalles(recibo.id_recibo)}
                                        className="btn-detalles"
                                        disabled={loadingRecibo[recibo.id_recibo]}
                                    >
                                        {loadingRecibo[recibo.id_recibo] ? 'Cargando...' : 'Ver Detalles'}
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            {modalVisible && (
                <div className="modal" role="dialog" aria-labelledby="modalTitle" aria-modal="true">
                    <div className="modal-content">
                        <span className="close" onClick={closeModal} role="button" tabIndex="0" aria-label="Cerrar">
                            &times;
                        </span>
                        <h2 id="modalTitle">Detalles del Recibo</h2>
                        {pdfUrl ? (
                            <iframe src={pdfUrl} width="100%" height="600px" title="Recibo PDF"></iframe>
                        ) : (
                            <p>Cargando el recibo...</p>
                        )}
                    </div>
                </div>
            )}
        </div>
    );
};

export default Recibos;
