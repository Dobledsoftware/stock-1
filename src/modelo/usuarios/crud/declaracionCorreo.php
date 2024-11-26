<?php
include "../../../controlador/Usuarios.php";
$email=$_POST['email'];
$email2=$_POST['email2'];
$cuil=$_POST['cuil'];
$id_usuario=$_POST['id_usuario'];  
$Usuarios = new Usuarios();
echo $Usuarios->declaracionCorreo($id_usuario,$cuil,$email,$email2); 
?>




