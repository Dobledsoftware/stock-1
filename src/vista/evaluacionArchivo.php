<?php
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    if (isset($_FILES['pdf']) && $_FILES['pdf']['error'] == UPLOAD_ERR_OK) {
        // Obtener detalles del archivo
        $fileTmpPath = $_FILES['pdf']['tmp_name'];
        $fileName = $_FILES['pdf']['name'];
        $fileSize = $_FILES['pdf']['size'];
        $fileType = $_FILES['pdf']['type'];
        $fileNameCmps = explode(".", $fileName);
        $fileExtension = strtolower(end($fileNameCmps));
        // Comprueba la extensión del archivo
        $allowedfileExtensions = array('pdf');
        if (in_array($fileExtension, $allowedfileExtensions)) {
            // Ruta donde se guardará el archivo
            $uploadFileDir = '../public/pdf/sabana/';
            $dest_path = $uploadFileDir . $fileName;
            //echo $dest_path;
            if(move_uploaded_file($fileTmpPath, $dest_path)) {
                        $parametro1 = $dest_path;
                        //$parametro2 = '/opt/recibos/periodos/';
                        $script_path = 'python3 ../count_recibos.py';
                        // Ejecutar el script con parámetros
                        //echo $parametro1;
                        $command = escapeshellcmd("$script_path $parametro1") . " 2>&1";
                        $output = [];
                        $return_var = 0;
                        $caputra=exec($command, $output, $return_var);
                        // Mostrar la salida del script
                        /* echo "<pre>" . implode("\n", $output) . "</pre>"; */
                        // Verificar el código de retorno                      
//echo "Command: $command\n";
//echo "Return var: $return_var\n";
$jsonOutput = implode("\n", $output);
/* echo $parametro1; */
//echo $output;
// Verificar si la salida es un JSON válido
$data = json_decode($jsonOutput, true);
if (json_last_error() === JSON_ERROR_NONE) {
  // Obtener solo el nombre del archivo
  $file_name = basename($dest_path);
  // Agregar el nombre del archivo al JSON
  $data['file_name'] = $file_name;

    echo json_encode($data);
} else {
    // Manejar el error de parseo JSON
    echo json_encode(['error' => 'Invalid JSON from Python script']);
}
} else {
echo json_encode(['error' => 'Error moving the uploaded file']);
}
} else {
echo json_encode(['error' => 'Invalid file extension']);
}
} else {
echo json_encode(['error' => 'File upload error']);
}
} else {
echo json_encode(['error' => 'Invalid request method']);
}
?>
