<?php
// Archivo: ../modelo/recibos/crud/abrirRecibo.php
// Verificar que se haya hecho una solicitud POST
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Verificar que la ruta del archivo esté presente en la solicitud
    if (isset($_POST['archivo'])) {
        $archivo = $_POST['archivo'];
        ini_set('display_errors', 1);
        ini_set('display_startup_errors', 1);
        error_reporting(E_ALL);
        // Ruta completa al archivo       
        // Ruta base del directorio del archivo
        $ruta_base = realpath(__DIR__ . '/../../../public/pdf');
        // Ruta completa al archivo
        $ruta_completa = $ruta_base  . $archivo;
        // Comprobación adicional
        //echo "Ruta del archivo: " . $ruta_completa . "<br>";

        // Verificar que el archivo existe
        if (file_exists($ruta_completa)) {           
            // Enviar los encabezados adecuados para la visualización del PDF
            header('Content-Type: application/pdf');
            header('Content-Disposition: inline; filename="' . basename($ruta_completa) . '"');
            readfile($ruta_completa);
            exit;
        } else {
            echo "Archivo no encontrado.";
        }
    } else {
        // No se proporcionó la ruta del archivo
        echo "Ruta del archivo no proporcionada.";
    }
} else {
    // No se hizo una solicitud POST
    echo "Método no permitido.";
}
?>

