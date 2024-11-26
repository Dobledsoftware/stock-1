<?php
 session_start(); 
//solo administrador del sistema
if(isset($_SESSION['cuil']) and ($_SESSION['rol'] == 2) or($_SESSION['rol'] == 1)or($_SESSION['rol'] == 3)){
include "../header.php";
include "../footer.php";
?>
<link rel="stylesheet" href="../public/css/mi_info.css">

    <div class="container2">
        <h2>Usuario</h2>
        <br>
        <div class="user-details">
            <label hidden>ID:</label>
            <span id="userId" hidden></span>
        </div>
        <div class="user-details">
            <label>CUIL:</label>
            <span id="userCuil"></span>
        </div>
        <!-- <div class="user-details">
            <label>Nombre y Apellido concatenado:</label>
            <span id="userApellidoYNombreConcatenado"></span>
        </div> -->
        <div class="user-details">
            <label>Nombre:</label>
            <span id="userName"></span>
        </div>
        <div class="user-details">
            <label>Apellido:</label>
            <span id="userLastName"></span>
        </div>      
        <div class="user-details">
            <label>Legajo:</label>
            <span id="userLegajo"></span>
        </div>
        <div class="user-details">
            <label>Correo Electrónico:</label>
            <span id="userEmail"></span>
        </div>
    </div>
    <script src="../public/js/usuarios/misDatos.js"></script>
    <script>
        // Llama a la función con el ID de usuario deseado
        $(document).ready(function() {
            var id_usuario = <?php echo $_SESSION['id_usuario']; ?>;
            misDatos(id_usuario); 
        });
    </script>
<?php
}
else 
{
    session_start();
    session_destroy();
    header("Location: ../index.php");
    exit();

}

?>