<?php
    $email = $_POST['email'];
    $email2 = $_POST['email2'];
    include "../../../clases/Usuarios.php";
    $Usuarios = new Usuarios();

    echo $Usuarios->verificacionRestablecerContrasenia($email,$email2);
?>