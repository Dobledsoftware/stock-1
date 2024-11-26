<?php  
    $cuil= $_POST['cuilNewUser'];
    $nombre = $_POST['nombreNewUser'];
    $apellido= $_POST['apellidoNewUser'];
    $legajo= $_POST['legajoNewUser'];
    $email = $_POST['emailNewUser'];
    $rol=1;
    
include "../../../controlador/Usuarios.php";
$Usuarios = new Usuarios(); 
echo $Usuarios->agregaNuevoUsuario($cuil,$nombre,$apellido,$rol,$legajo,$email);
?>
    

