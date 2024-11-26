<?php
session_start();
    $id_usuario = $_POST['id_usuario'];
    include "../../../controlador/Usuarios.php";
    $Usuarios = new Usuarios();
    //echo json_encode(array('error' => 'entro al back'+$id_usuario));
      echo $Usuarios->misDatos($id_usuario); 
?>