<?php
// Importar la biblioteca FPDI fuera de la función
require_once('../public/fpdi/src/autoload.php');
use setasign\Fpdi\Fpdi;

function cortar_pdf_por_cuils($archivo_entrada, $directorio_salida) {
    $pdf = new Fpdi();
    $num_paginas = $pdf->setSourceFile($archivo_entrada);

    for ($pagina = 1; $pagina <= $num_paginas; $pagina++) {
        $pdf->AddPage();
        $pagina_id = $pdf->importPage($pagina);

        // Obtener el texto de la página actual
        $texto = $pdf->getPageContent();
        // Buscar el CUIL en el texto
        preg_match('/CUIL: (\d{2}-\d{8}-\d{1})/', $texto, $matches);
        $cuil = $matches[1] ?? 'sin_cuil';

        // Obtener la fecha actual
        $fecha_actual = date('Y-m-d');

        // Guardar la página en un PDF separado según el CUIL y la fecha
        $pdf->useTemplate($pagina_id);
        $nombre_pdf = "$directorio_salida/$cuil-$fecha_actual-pagina$pagina.pdf";
        $pdf->Output($nombre_pdf, 'F');

        
    }
}

// configuracion de uso
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_FILES['pdfInput'])) {
    $archivo_entrada = $_FILES['pdfInput']['tmp_name'];
    $directorio_salida = 'pdfs_por_usuarios';
    if (!is_dir($directorio_salida)) {
        mkdir($directorio_salida);
    }

    // Llamar a la función cortar_pdf_por_cuils
    cortar_pdf_por_cuils($archivo_entrada, $directorio_salida);
    echo 'PDF cortado y almacenado correctamente.';
} else {
    header('HTTP/1.1 400 Bad Request');
    echo 'Error en la solicitud.';
}
?>
