<?php
session_start();
$id_usuario = $_SESSION['id_usuario'];
// solo administrador del sistema
if (isset($_SESSION['cuil']) && ($_SESSION['rol'] == 2) || ($_SESSION['rol'] == 1)) {
    include "../header.php";
    include "../footer.php";
?>
<!-- Incrustar las variables de sesión en un div oculto -->
<div id="sessionData" style="display: none;" data-id_usuario="<?php echo $id_usuario; ?>"></div>

<select id="periodo" class="filter-select">
    <option value="">Seleccione Periodo</option>
    <option value="042024">Abril 2024</option>
    <option value="052024">Mayo 2024</option>
    <option value="062024">Junio 2024</option>
    <option value="072024">Julio 2024</option>
    <option value="082024">Agosto 2024</option>
    <option value="092024">Septiembre 2024</option>
    <option value="102024">Octubre 2024</option>
    <option value="112024">Noviembre 2024</option>
    <option value="122024">Diciembre 2024</option>
</select>
<br><br>

<table id="tablaRecibosDataTable" class="display table table-sm dt-responsive nowrap my-custom-table" style="width:100%">
    <thead>
        <tr>
            <th>Recibo</th>
            <th>Periodo</th>
            <th>Acciones</th>
        </tr>
    </thead>
    <tbody></tbody>
</table>

<div id="pdfContainer" style="display: none;">
    <embed id="pdfEmbed" src="" width="600" height="500" type="application/pdf">
</div>

<!-- Asegúrate de cargar jQuery primero -->
<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
<!-- Incluye los archivos JS de DataTables -->
<script src="https://cdn.datatables.net/1.11.5/js/jquery.dataTables.min.js"></script>
<script src="https://cdn.datatables.net/responsive/2.2.9/js/dataTables.responsive.min.js"></script>
<!-- Incluye los archivos CSS de DataTables -->
<link rel="stylesheet" href="https://cdn.datatables.net/1.11.5/css/jquery.dataTables.min.css">
<link rel="stylesheet" href="https://cdn.datatables.net/responsive/2.2.9/css/responsive.dataTables.min.css">

<script>
    $(document).ready(function() {
        var id_usuario = <?php echo json_encode($id_usuario); ?>;
        $('#periodo').on('change', function() {
            var periodoSeleccionado = $(this).val();
            console.log(periodoSeleccionado);
            cargarTablaRecibos(id_usuario, periodoSeleccionado);
        });
    });

    function cargarTablaRecibos(id_usuario, periodo) {
        if ($.fn.DataTable.isDataTable('#tablaRecibosDataTable')) {
            $('#tablaRecibosDataTable').DataTable().destroy();
        }
        $('#tablaRecibosDataTable').DataTable({
            "processing": true,
            "serverSide": true,
            "ajax": {
                "url": "../modelo/recibos/crud/cargaTablaRecibos.php",
                "type": "POST",
                "data": {
                    "cuil": id_usuario,
                    "periodo": periodo
                },
                "dataSrc": function(json) {
                    console.log(json.data); // Verificar los datos en la consola
                    if (json.data) {
                        return json.data;
                    } else {
                        console.error('No se recibieron datos desde el servidor.');
                        return [];
                    }
                },
                "error": function(jqXHR, textStatus, errorThrown) {
                    console.error('Se produjo un error al intentar obtener los datos.', jqXHR.responseText);
                }
            },
            "columns": [
                { "data": "descripcion_archivo" },
                { "data": "periodo" },
                {
                    "data": "id_recibo",
                    "render": function(data, type, row, meta) {
                        return '<button class="btn btn-warning btn-sm" onclick="verRecibos(\'' + data + '\')">Ver</button>';
                    }
                }
            ],
            "createdRow": function(row, data, dataIndex) {
                // Aplica estilos personalizados a las filas o celdas
                $(row).css('background-color', '#f9f9f9');
                $(row).find('td:eq(0)').css('font-weight', 'bold');
            },
            "initComplete": function(settings, json) {
                // Aplica estilos adicionales después de que la tabla ha sido inicializada
                $('#tablaRecibosDataTable_wrapper').addClass('my-custom-style'); // Clase personalizada para el contenedor de la tabla
                $('#tablaRecibosDataTable_length').addClass('my-custom-length'); // Clase personalizada para el selector de longitud
                $('#tablaRecibosDataTable_filter').addClass('my-custom-filter'); // Clase personalizada para el filtro
            }
        });
    }
</script>

<style>
.my-custom-style {
    margin: 20px;
}

.my-custom-length select {
    width: 50px;
    background-color: #e0e0e0;
    border-radius: 5px;
}

.my-custom-filter input {
    width: 150px;
    background-color: #e0e0e0;
    border-radius: 5px;
}

.my-custom-table {
    border: 1px solid #ddd;
    font-size: 14px;
}

.my-custom-table thead {
    background-color: #f1f1f1;
}

.my-custom-table tbody tr:hover {
    background-color: #f1f1f1;
}
</style>

<?php
} else {
    session_start();
    session_destroy();
    header("Location: ../index.php");
    exit();
}
?>
