function cargarTablaRecibos(id_usuario, periodo) {
    if ($.fn.DataTable.isDataTable('#tablaRecibosDataTable')) {
        $('#tablaRecibosDataTable').DataTable().destroy();
    }
    $('#tablaRecibosDataTable').DataTable({
        "language": {
            "url": "/path/to/Spanish.json"
        },
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
      
    });
}



function verRecibos(id_recibo) {
    /*  var id_usuario = document.getElementById("sessionData").dataset.id_usuario; */
    $.ajax({
        url: '../modelo/recibos/crud/verRecibos.php',
        method: 'POST',
        data: { id_recibo: id_recibo },
        success: function(response) {
            console.log(response);
            var data = JSON.parse(response);
            console.log("respuesta ajax" + data)
            if (data && data.data && data.data.length > 0) {
                var ruta_archivo_completa = data.data[0].archivo;
                var nombre_archivo = ruta_archivo_completa.split('/').pop(); // Obtener solo el nombre del archivo
                var ruta_completa = '../public/pdf/' + nombre_archivo;
                console.log("ruta completa: " + ruta_completa);
                window.open(ruta_completa, '_blank');
            } else {
                console.log("La respuesta del servidor no contiene la URL del recibo.");
            }
        },
        error: function(xhr, status, error) {
            console.log("Error al obtener la URL del recibo:", error);
        }
    });
}