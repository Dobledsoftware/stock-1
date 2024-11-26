<?php
include "../../../controlador/Recibos.php";
$id_usuario= $_POST['id_usuario'];
$periodo = $_POST['periodo'];
$cuil= $_POST['cuil'];
    $Recibos = new Recibos(); 
echo $Recibos->cargaTablaRecibos($id_usuario,$periodo,$cuil);

   
 ?>
