<?php

    session_start();

    $usuario = $_POST['cuil'];
    $password = $_POST['password'];

    include "../../../controlador/Usuarios.php";
    $Usuarios = new Usuarios();

    echo $Usuarios->loginUsuario($usuario, $password);
?>