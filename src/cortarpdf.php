<?php
require 'vendor/autoload.php';
require 'vendor/fpdi/src/autoload.php';
require 'vendor/tcpdf/tcpdf.php';


use setasign\Fpdi\Fpdi;
use Smalot\PdfParser\Parser;

function processPdf($pdfPath, $outputDir) {
    // Crear instancia de FPDI
    $pdf = new FPDI();

    // Cargar el archivo PDF
    $pageCount = $pdf->setSourceFile($pdfPath);

    // Procesar cada página
    for ($pageNo = 1; $pageNo <= $pageCount; $pageNo++) {
        $pdf->AddPage();
        $tplId = $pdf->importPage($pageNo);
        $pdf->useTemplate($tplId);

        // Obtener el texto de la página
        $parser = new Parser();
        $pdfParsed = $parser->parseFile($pdfPath);
        $pages = $pdfParsed->getPages();
        $text = $pages[$pageNo - 1]->getText();

        // Buscar el identificador de usuario (Ej: ID: 12345)
        preg_match('/ID: (\d+)/', $text, $matches);
        if (isset($matches[1])) {
            $userId = $matches[1];
            $userDir = $outputDir . DIRECTORY_SEPARATOR . $userId;
            if (!is_dir($userDir)) {
                mkdir($userDir, 0777, true);
            }

            // Guardar la página en un nuevo PDF
            $newPdf = new FPDI();
            $newPdf->AddPage();
            $tplId = $newPdf->importPage($pageNo);
            $newPdf->useTemplate($tplId);
            $newPdfPath = $userDir . DIRECTORY_SEPARATOR . "page_$pageNo.pdf";
            $newPdf->Output($newPdfPath, 'F');
        }
    }
}

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_FILES['pdf'])) {
    $pdfPath = $_FILES['pdf']['tmp_name'];
    $outputDir = 'output'; // Directorio de salida
    processPdf($pdfPath, $outputDir);
    echo "El PDF ha sido procesado exitosamente.";
}
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Procesar PDF</title>
</head>
<body>
    <form action="process_pdf.php" method="post" enctype="multipart/form-data">
        <input type="file" name="pdf" accept="application/pdf">
        <button type="submit">Cargar PDF</button>
    </form>
</body>
</html>