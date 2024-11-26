<?php
  include "../../../controlador/Usuarios.php";
    
    $Usuarios = new Usuarios(); 
echo $Usuarios->cargaTablaUsuarios();


