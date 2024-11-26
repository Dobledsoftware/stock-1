<?php  
    $cuil= $_POST['cuil'];
    $nombre = $_POST['nombre'];
    $apellido= $_POST['apellido'];
    $rol= $_POST['rol'];
    $legajo= $_POST['legajo'];
    $email = $_POST['email'];
include "../../../controlador/Recibos.php";
$Recibos = new Recibos(); 
echo $Recibos->agregaNuevoRecibo($cuil,$nombre,$apellido,$rol,$legajo,$email);

?>
    

