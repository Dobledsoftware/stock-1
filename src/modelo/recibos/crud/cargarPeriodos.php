<?php
include "../../../controlador/Recibos.php";
$id_usuario= $_POST['id_usuario'];
$cuil= $_POST['cuil'];
    $Recibos = new Recibos(); 
echo $Recibos->cargarPeriodos($id_usuario,$cuil);

   
 ?>
