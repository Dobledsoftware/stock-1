<?php
include "../../../controlador/Usuarios.php";
$pass=$_POST['pass'];
$pass2=$_POST['pass2'];
$id_usuario=$_POST['id_usuario'];  
$Usuarios = new Usuarios();
echo $Usuarios->nuevoPass($pass,$pass2,$id_usuario); 
?>




