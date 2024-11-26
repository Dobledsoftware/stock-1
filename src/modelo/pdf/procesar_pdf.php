<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_FILES['archivo'])) {
    $archivo_entrada = $_FILES['archivo']['tmp_name'];
    $directorio_salida = 'pdfs_cortados';

    require_once('cortar_pdf.php');
    cortar_pdf_por_cuils($archivo_entrada, $directorio_salida);

    // Aquí deberías tener código para guardar la información en la base de datos
    // Ejemplo:
    // $pdf_cortado = obtener_nombres_archivos($directorio_salida);
    // guardar_en_base_de_datos($pdf_cortado);

    echo 'PDF cargado y cortado correctamente.';
} else {
    header('HTTP/1.1 400 Bad Request');
    echo 'Error en la solicitud.';
}
?>
