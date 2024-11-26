<?php


    $password = $_POST['password'];
   /*  $passwordh = password_hash($password, PASSWORD_BCRYPT); */
    $password2 = $_POST['password2'];
    /* $passwordh2 = password_hash($password2, PASSWORD_BCRYPT); */
    $email=$_POST['email'];
    $tokken_pass=$_POST['tokken_pass'];
    include "../../../clases/Usuarios.php";
    $Usuarios = new Usuarios();

    echo $Usuarios->verificacionRestablecerContraseniaConTokken($password,$password2,$email,$tokken_pass);
?>