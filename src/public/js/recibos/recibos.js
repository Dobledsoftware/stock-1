function cargarTablaRecibos(id_usuario, periodo,cuil) {
    if ($.fn.DataTable.isDataTable('#tablaRecibosDataTable')) {
        $('#tablaRecibosDataTable').DataTable().destroy();
    }
    $('#tablaRecibosDataTable').DataTable({
        "language": {
            "url": "https://cdn.datatables.net/plug-ins/1.10.15/i18n/Spanish.json"
        },
        "processing": true,
        "serverSide": true,
        "ajax": {
            "url": "../modelo/recibos/crud/cargaTablaRecibos.php",
            "type": "POST",
            "data": {
                "id_usuario": id_usuario,
                "periodo": periodo,
                "cuil": cuil
            },
            "dataSrc": function(json) {                
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
        "data": "id_recibo", //trae variable del back
        "render": function(data, type, row, meta) {
            return '<div style="position: relative; display: inline-block;">' +
                   '<button class="btn btn-warning btn-sm" onclick="verRecibos(\'' + data + '\')">Ver</button>' +
                   '<i class="fas fa-info-circle info-icon">' +
                   '<div class="tooltip">En caso de no visualizar el archivo, verifique los permisos del navegador</div>' +
                   '</i>' +
                   '</div>';
        }
    }
]
  });
}




function verRecibos(id_recibo) {
    /*  var id_usuario = document.getElementById("sessionData").dataset.id_usuario; */
    $.ajax({
        url: '../modelo/recibos/crud/verRecibos.php',
        method: 'POST',
        data: { id_recibo: id_recibo },
        success: function(response) {     
            var data = JSON.parse(response);
            if (data && data.data && data.data.length > 0) {
                 // Obtener la carpeta y la ruta completa del archivo
                 var archivo = data.data[0].archivo;
                 //var carpeta = archivo.split('/').slice(0, -1).join('/'); // Obtener la carpeta
                 //var nombre_archivo = archivo.split('/').pop(); // Obtener solo el nombre del archivo
                 
                 // Construir la ruta completa al archivo PDF en la carpeta pública
                 //var ruta_completa = '../public/pdf' + archivo;

                 // Imprimir la carpeta y el nombre del archivo en la consola
                /*  console.log("Carpeta: " + carpeta);
                 console.log("Nombre del archivo: " + nombre_archivo); */

                 // Abrir el archivo en una nueva pestaña
                // window.open(ruta_completa, '_blank');
                  // Crear un formulario temporal
                  var form = document.createElement("form");
                  form.method = "POST";
                  form.action = '../modelo/recibos/crud/abrirRecibo.php';
                  form.target = "_blank";
                  
                  // Crear un campo oculto para la URL del recibo
                  var input = document.createElement("input");
                  input.type = "hidden";
                  input.name = "archivo";
                  input.value = archivo;  
                  // Añadir el campo al formulario
                  form.appendChild(input);  
                  // Añadir el formulario al body y enviarlo
                  document.body.appendChild(form);
                  form.submit();  
                  // Eliminar el formulario del DOM
                  document.body.removeChild(form);
                 
            } else {
                console.log("La respuesta del servidor no contiene la URL del recibo.");
            }
        },
        error: function(xhr, status, error) {
            console.log("Error al obtener la URL del recibo:", error);
        }
    });
}

/* function cargarPeriodos(id_usuario) {
    $.ajax({
        url: "../modelo/recibos/crud/cargarPeriodos.php",
        type: "POST",
        data: {id_usuario: id_usuario},
        success: function(data) {
            var periodos = JSON.parse(data);
            var select = $('#periodo');
            select.empty();
            select.append('<option value="">Seleccione Periodo</option>');
            periodos.forEach(function(periodo) {
                select.append('<option value="' + periodo + '">' + periodo + '</option>');
            });
        },
        error: function(jqXHR, textStatus, errorThrown) {
            console.error('Error al cargar los periodos:', errorThrown);
        }
    });
}




 */

function cargarPeriodos(id_usuario,cuil) {
    $.ajax({
        url: "../modelo/recibos/crud/cargarPeriodos.php",
        type: "POST",
        data: { id_usuario: id_usuario,cuil: cuil },
        success: function(data) {
            var periodos = JSON.parse(data);
            var select = $('#periodo');
            select.empty();
            select.append('<option value="">Seleccione Periodo</option>');
            periodos.forEach(function(periodo) {
                // Extrae el mes y el año de la cadena
                var mes = periodo.substring(0, 2);
                var año = periodo.substring(2, 6);
                // Formatea la cadena
                var periodoFormateado = mes + '/' + año;
                // Añade la opción al select
                select.append('<option value="' + periodo + '">' + periodoFormateado + '</option>');
            });
        },
        error: function(jqXHR, textStatus, errorThrown) {
            console.error('Error al cargar los periodos:', errorThrown);
        }
    });
}

