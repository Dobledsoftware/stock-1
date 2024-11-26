<?php
include "../../../controlador/Usuarios.php";
$id_usuario=$_POST['id_usuario']; 
$cuil=$_POST['cuil'];
//$email=$_POST['email'];
$codigo=$_POST['codigo']; 
$Usuarios = new Usuarios();
echo $Usuarios->validacionCorreo($id_usuario,$cuil,$codigo); 
?>


