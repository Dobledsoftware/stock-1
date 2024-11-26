<?php        
                $id_usuario= $_POST['id_usuarioUpdate'];
                $cuil=$_POST['cuilUpdate'];
                $nombre= $_POST['nombreUpdate'];
                $apellido=$_POST['apellidoUpdate'];
                $legajo=$_POST['legajoUpdate'];
                $email=$_POST['correoUpdate'];
                $rol=$_POST['rolUpdate']; 
        include "../../../controlador/Usuarios.php";
        $Usuario = new Usuarios();
        echo $Usuario -> editarUsuario($id_usuario,$cuil,$nombre,$apellido,$legajo,$email,$rol);
?>
