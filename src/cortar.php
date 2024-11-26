<?php
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

        // Aquí podrías agregar código para insertar la información en una base de datos
    }
}

// Ejemplo de uso
$archivo_entrada = 'archivo.pdf';
$directorio_salida = 'pdfs_por_usuarios';
if (!is_dir($directorio_salida)) {
    mkdir($directorio_salida);
}
cortar_pdf_por_cuils($archivo_entrada, $directorio_salida);
echo 'PDF cortado y almacenado correctamente.';
?>
