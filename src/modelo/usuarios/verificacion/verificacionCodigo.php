<?php
    $email = $_POST['email'];
    $codigo = $_POST['codigo'];
    include "../../../clases/Usuarios.php";
    $Usuarios = new Usuarios();

    echo $Usuarios->verificacionCodigo($email,$codigo);
?>