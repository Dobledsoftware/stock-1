<?php
session_start();
//solo administrador del sistema
if(isset($_SESSION['cuil']) and (($_SESSION['rol'] == 2)or($_SESSION['rol'] == 3))){
include "../header.php";
include "../footer.php";
?>
<style>
        #cargarBtn:disabled {
            background-color: #ccc; /* Color gris */
            color: #666; /* Texto gris oscuro */
            cursor: not-allowed; /* Cursor no permitido */
        }
        #result {
            margin-top: 20px;
        }
        #result .data {
            margin-bottom: 10px;
        }
        #result .buttons {
            display: flex;
            gap: 10px;
        }
    </style>
<link rel="stylesheet" href="../public/css/carga.css">
    <div class="container3">
        <h2>Importar PDFs</h2>
        <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Subir PDF</title>
</head>
<body>
    <h2>Seleccionar PDF para Cortar</h2>
    <form id="uploadForm" enctype="multipart/form-data">
        <input type="file" id="pdfInput" name="pdf" accept="application/pdf" ">
        <input type="submit" value="Importar PDF" id="cargarBtn" disabled>
    </form>
    <div id="result"></div>
    <div id="mensaje"></div>
    <script src="https://code.jquery.com/jquery-3.5.1.min.js"></script>    
    <script>      
    
 $(document).ready(function() {
    $('#pdfInput').on('change', function(event) {
        var file = event.target.files[0];
        if (file) {
            var formData = new FormData();
            formData.append('pdf', file);
            $.ajax({
                url: 'evaluacionArchivo.php', // Cambia esto por la URL de tu backend
                type: 'POST',
                data: formData,
                processData: false,
                contentType: false,
                timeout: 600000, // Timeout de 10 minutos en milisegundos
                success: function(response) {
                    //console.log("salida: " +JSON.parse(response)); 
                    try {
                        var data = JSON.parse(response);
                        fileName = data.file_name; // Guarda el nombre del archivo
                        displayResult(data);
                    } catch (error) {
                        console.error('Error parsing JSON:', error);
                        alert('Error al procesar la respuesta del servidor'+response);
                    }
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    if (textStatus === 'timeout') {
                        alert('La solicitud ha excedido el tiempo de espera de 10 minutos.');
                    } else {
                        alert('Hubo un error al procesar el archivo: ' + errorThrown);
                    }
                }
            });
        }
    });
    function displayResult(data) {
                // Extrae el mes y el año de la cadena
            var mes = data.periodo.substring(0, 2);
            var año = data.periodo.substring(2, 6);
            // Formatea la cadena
            var periodoFormateado = mes + '/' + año;

        Swal.fire({
            title: 'Resultado de la Evaluación del archivo principal.',
            html: `<p style="font-size: 20px; text-align: center;">Cantidad de recibos de sueldos: ${data.count}</p>
                   <p style="font-size: 20px; text-align: center;">Periodo: ${periodoFormateado}</p>
                   <p style="font-size: 20px; text-align: center;">Nombre del archivo: ${data.file_name}</p>
                   <p style="font-size: 20px; text-align: center;">¿Usted está seguro de continuar?</p>`,
            showCancelButton: true,
            confirmButtonText: 'Sí',
            cancelButtonText: 'No',
            customClass: {
                title: 'my-title-class',
                htmlContainer: 'my-html-container-class',
                confirmButton: 'my-confirm-button-class',
                cancelButton: 'my-cancel-button-class'
            },
            allowOutsideClick: false // Asegura que no se puede hacer clic fuera del modal
        }).then((result) => {
            if (result.isConfirmed) {
                $('#cargarBtn').prop('disabled', false); // Habilita el botón "Importar PDF"
            } else if (result.dismiss === Swal.DismissReason.cancel) {
                $('#cargarBtn').prop('disabled', true); // Deshabilita el botón "Importar PDF"
                $('#pdfInput').val(''); // Resetea el input de archivo
                $('#result').empty();
            }
        });
    }
    $('#uploadForm').on('submit', function(event) {
        event.preventDefault();
        Swal.fire({
            title: '¿Está seguro de continuar?',
            text: "¿Desea continuar con la carga del archivo?",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: 'Sí',
            cancelButtonText: 'No',
            allowOutsideClick: false
        }).then((result) => {
            if (result.isConfirmed) {
                    Swal.fire({
                    title: 'Procesando...',
                    text: 'Por favor, espere.',
                    allowOutsideClick: false,
                    didOpen: () => {
                        Swal.showLoading();
                    }
                });
                var formData = new FormData(this);
                formData.append('file_name', fileName); // Agregar el nombre del archivo al FormData
                $.ajax({
                    url: 'upload_pdf.php', // Ruta al script PHP que maneja la subida
                    type: 'POST',                    
                    data: formData,
                    contentType: false,
                    processData: false,
                    timeout: 600000, // Timeout de 10 minutos en milisegundos
                    success: function(response) {
                        console.log(response);                        
                            Swal.close(); // Cierra el SweetAlert de procesando
                            if(response==0){
                            Swal.fire({
                                title: 'Éxito',
                                text: 'El proceso se ejecutó correctamente.',
                                icon: 'success',
                                confirmButtonText: 'Ok',
                                allowOutsideClick: false
                            }).then(() => {
                                location.reload(); // Recarga la página después de mostrar el mensaje de éxito
                            });
                        }
                    },
                    error: function(jqXHR, textStatus, errorThrown) {
                        if (textStatus === 'timeout') {
                        alert('La solicitud ha excedido el tiempo de espera de 10 minutos.');
                        }
                        Swal.close(); // Cierra el SweetAlert de procesando en caso de error
                        Swal.fire({
                            title: 'Error',
                            text: 'Error al cargar el archivo: ' + errorThrown,
                            icon: 'error',
                            confirmButtonText: 'Ok',
                            allowOutsideClick: false
                        });
                    }
                });
            }
        });
    });
});
</script>
</body>              
    </div>
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
