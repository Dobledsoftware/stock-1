<?php
include "../../../controlador/Recibos.php";
$id_recibo= $_POST['id_recibo'];
    $Recibos = new Recibos(); 
echo $Recibos->verRecibos($id_recibo);
 
   
 ?>
