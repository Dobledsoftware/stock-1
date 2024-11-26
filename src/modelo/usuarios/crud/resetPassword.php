<?php
    $id_usuario=$_POST['id_usuario'];  
    include "../../../controlador/Usuarios.php";
    $Usuarios = new Usuarios();
    echo $Usuarios->resetPassword($id_usuario) ;
?>