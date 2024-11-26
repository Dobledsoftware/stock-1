<?php
   /*  if (isset($_FILES['pdf']) && $_FILES['pdf']['error'] == UPLOAD_ERR_OK) {
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
            // Ruta donde se guardará el archivo */
            $archivo=$_POST['file_name'];
            $uploadFileDir = '../public/pdf/sabana/';
            $dest_path = $uploadFileDir . $archivo;
                        /* echo $_FILES;*/
                        $parametro1 = $dest_path;
                        $parametro2 = '../public/pdf/';
                        $script_path = '../parcer_recibos_sueldo.py';/////var/www/recibos/public/recibos.sh
                        //echo  'Entro'; 
			// Ejecutar el script con parámetros
			//
                        //$command = escapeshellcmd("$script_path $parametro1 $parametro2") . " 2>&1";
			
                        $command = escapeshellcmd("python3 $script_path $parametro1 $parametro2") . " 2>&1";
			//echo $command;
			$output = [];
                        $return_var = 0;
			/* print $parametro1 . $parametro2; */ 
			exec($command, $output, $return_var);
			//echo $return_var;
                        // Mostrar la salida del script
                        //echo "<pre>" . implode("\n", $output) . "</pre>";
                        // Verificar el código de retorno
                        if ($return_var === 0) {
                            return 0;                                  
                            //configuramos el retorno para la carteleria ajax
                        } else {
                            return 1;
                        }
/* 
            } else {
                echo 'Hubo un problema al mover el archivo a la carpeta de destino.';
            }
        } else {
            echo 'Solo se permiten archivos con extensión PDF.';
        }
    } else {
        echo 'Hubo un error al subir el archivo.';
    } */

?>
