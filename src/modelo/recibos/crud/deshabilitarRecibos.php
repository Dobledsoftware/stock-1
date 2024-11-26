<?php
    $dni=$_POST['dni']; 
    include "../../../clases/Usuarios.php";
    $Usuarios = new Usuarios();
    echo $Usuarios->deshabilitarUsuarios($cuil);
?>