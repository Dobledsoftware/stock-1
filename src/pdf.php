<?php
require_once 'src/Fpdf/fpdf.php';
require_once 'src/setasign/Fpdi/Fpdi.php';
require_once 'src/setasign/Fpdi/PdfReader/PdfReader.php';
require_once 'src/setasign/Fpdi/PdfParser/StreamReader.php';

use setasign\Fpdi\Fpdi;
use setasign\Fpdi\PdfReader\PdfReader;
use setasign\Fpdi\PdfParser\StreamReader;

// Conexión a la base de datos
$servername = "10.5.0.7";
$username = "dario";
$password = "Dar10";
$dbname = "newApp";

$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
    die("Conexión fallida: " . $conn->connect_error);
}

// Obtén los argumentos de la línea de comandos
$ifn = $argv[1];
$ofn = $argv[2];

// Función para extraer texto de una área específica de la página PDF
function extract_text_from_area($pdf, $pageNumber) {
    // Utiliza FPDI para leer y extraer texto
    $pdf->AddPage();
    $pageId = $pdf->importPage($pageNumber);
    $pdf->useTemplate($pageId);

    $text = array();

    // Coordenadas para extraer texto
    $text['name'] = $pdf->getText(100, 100, 250, 115);
    $text['cuil'] = str_replace('-', '', $pdf->getText(250, 100, 350, 115));
    $text['periodo'] = str_replace('/', '', $pdf->getText(40, 160, 100, 170));
    $text['description'] = $pdf->getText(120, 160, 310, 170);

    return $text;
}

// Abre el PDF con FPDI
$pdf = new Fpdi();
$pageCount = $pdf->setSourceFile($ifn);
$fecha_subida = date('Y-m-d H:i:s');

for ($pageNumber = 1; $pageNumber <= $pageCount; $pageNumber++) {
    $dict = extract_text_from_area($pdf, $pageNumber);

    // Genera el nombre del archivo
    $pdf_name = $ofn . implode('_', array_map(function($v) {
        return str_replace([' ', ',', '/', '\n'], '', $v);
    }, $dict)) . '.pdf';

    // Guarda el nuevo archivo
    $pdf->Output($pdf_name, 'F');

    // Realiza las consultas a la base de datos
    $stmt = $conn->prepare("SELECT id_usuario FROM usuarios WHERE cuil = ?");
    $stmt->bind_param("s", $dict['cuil']);
    $stmt->execute();
    $result = $stmt->get_result();
    $id_usuario_list = $result->fetch_assoc();

    $stmt = $conn->prepare("SELECT id_recibo, periodo, descripcion_archivo FROM recibos WHERE periodo = ? AND descripcion_archivo = ? AND cuil = ?");
    $stmt->bind_param("sss", $dict['periodo'], $dict['description'], $dict['cuil']);
    $stmt->execute();
    $result = $stmt->get_result();
    $recivos_update = $result->fetch_assoc();

    if ($recivos_update) {
        $stmt = $conn->prepare("UPDATE recibos SET fecha_subida = ?, descripcion_archivo = ?, ruta_archivo = ? WHERE id_recibo = ?");
        $stmt->bind_param("sssi", $fecha_subida, $dict['description'], $pdf_name, $recivos_update['id_recibo']);
    } else {
        if ($id_usuario_list) {
            $id_usuario = $id_usuario_list['id_usuario'];
            $stmt = $conn->prepare("INSERT INTO recibos (id_usuario, periodo, fecha_subida, descripcion_archivo, ruta_archivo, cuil) VALUES (?, ?, ?, ?, ?, ?)");
            $stmt->bind_param("isssss", $id_usuario, $dict['periodo'], $fecha_subida, $dict['description'], $pdf_name, $dict['cuil']);
        } else {
            $stmt = $conn->prepare("INSERT INTO recibos (periodo, fecha_subida, descripcion_archivo, ruta_archivo, cuil) VALUES (?, ?, ?, ?, ?)");
            $stmt->bind_param("sssss", $dict['periodo'], $fecha_subida, $dict['description'], $pdf_name, $dict['cuil']);
        }
    }

    $stmt->execute();
    $stmt->close();
}

$conn->close();
?>
