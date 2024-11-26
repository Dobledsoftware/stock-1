<?php
 session_start(); 
//solo administrador del sistema
if(isset($_SESSION['cuil']) and ($_SESSION['rol'] == 2) or ($_SESSION['rol'] == 3)){
include "../header.php";
include "../footer.php";
?>
<link rel="stylesheet" href="../public/css/activacion.css">
 <script src="https://code.jquery.com/jquery-3.5.1.min.js"></script>


    <form id="consultaRecibosForm">
        <input type="text" id="cuil" placeholder="Ingrese CUIL" required>
        <button type="submit">Buscar</button>
    </form>

    <table id="tablaRecibos">
        <thead>
            <tr>
                <th>Periodo</th>
                <th>Descripción</th>
                <th>Estado</th>
                <th>Acciones</th>
            </tr>
        </thead>
        <tbody></tbody>
    </table>

    <div id="mensajeModal" class="modal">
        <div class="modal-content">
            <span class="close">&times;</span>
            <p id="mensajeTexto"></p>
        </div>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', function() {
            // Función para llenar la tabla con datos
            function populateTable(data) {
                const tableBody = document.querySelector('#tablaRecibos tbody');
                tableBody.innerHTML = ''; // Limpiar tabla antes de rellenar

                data.forEach(recibo => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        
                        <td>${recibo.periodo}</td>
                        <td>${recibo.descripcion_archivo}</td>
                        <td>${recibo.estado}</td>
                        <td>
                            <button class="${recibo.estado === 'Activado' ? 'desactivado' : 'activado'}" onclick="cambiarEstado('${recibo.id_recibo}', '${recibo.estado === 'Activado' ? 'desactivado' : 'activado'}')">
                                ${recibo.estado === 'Activado' ? 'Desactivar' : 'Activar'}
                            </button>
                        </td>
                    `;
                    tableBody.appendChild(row);
                });
            }

            // Función para buscar recibos
            document.getElementById('consultaRecibosForm').addEventListener('submit', function(e) {
                e.preventDefault();

                const cuil = document.getElementById('cuil').value;

                fetch(`${config.apiUrl}/todos_los_recibos`, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({ cuil: cuil })
})
.then(response => response.json())
.then(data => {
    if (data.length) {
        populateTable(data);
    } else {
        Swal.fire('No se encontraron recibos', '', 'info');
    }
})
.catch(error => console.error('Error detectado:', error)); // Verificar que todo esté cerrado

            });

            // Función para cambiar el estado de un recibo
            window.cambiarEstado = function(idRecibo, estado) {
                const url = estado === 'activado' ? '/activa_recibos' : '/desactiva_recibos';

                fetch(`${config.apiUrl}${url}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ id_recibo: idRecibo })
                })
                .then(response => response.json())
                .then(result => {
                    if (result.status === 'success') {
                        Swal.fire({
                            icon: 'success',
                            title: result.message,
                            showConfirmButton: false,
                            timer: 1500 // Cierra el alert automáticamente después de 1.5 segundos
                        }).then(() => {
                            // Refrescar tabla después de cerrar el alert
                            document.getElementById('consultaRecibosForm').dispatchEvent(new Event('submit'));
                        });
                    } else {
                        Swal.fire({
                            icon: 'error',
                            title: 'Error',
                            text: result.message
                        });
                    }
                })
                .catch(error => console.error('Error:', error));
            };
        });
    </script>
<script src="https://code.jquery.com/jquery-3.5.1.min.js"></script>
<script src="../config.js"></script>
<?php
}
else 
{
    session_start();
    session_destroy();
    header("Location: ../index.php");
    exit();

}

?>