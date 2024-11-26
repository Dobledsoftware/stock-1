<?php
    $id_usuario=$_POST['id_usuario']; 
    $cuil=$_POST['cuil']; 
    include "../../../controlador/Usuarios.php";
    $Usuarios = new Usuarios();
    echo $Usuarios->deshabilitarUsuario($id_usuario);
?>