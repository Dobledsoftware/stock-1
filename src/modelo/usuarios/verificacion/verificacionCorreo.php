<?php
    $email = $_POST['email'];
    $nombre=$_POST['nombre'];
    $apellido=$_POST['apellido'];
    $cuil=$_POST['cuil'];
    $password=$_POST['password'];
    $passwordh = password_hash($password, PASSWORD_BCRYPT);

// Luego, almacena el valor de $hash en tu base de datos junto con la sal.

    //$codigo = $_POST['codigo'];
    include "../../../clases/Usuarios.php";
    $Usuarios = new Usuarios();
    echo $Usuarios->verificacionCorreo($email,
    
    $nombre,
    $apellido,
    $cuil,
    $passwordh);/**/
?>