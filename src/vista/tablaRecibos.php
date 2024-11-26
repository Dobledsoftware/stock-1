<?php
 session_start();
 $id_usuario = $_SESSION['id_usuario'];
 $cuil=$_SESSION['cuil'];
//solo administrador del sistema
if(isset($_SESSION['cuil']) and ($_SESSION['rol'] == 2) or($_SESSION['rol'] == 1)or($_SESSION['rol'] == 3)){

// Verifica si el usuario ha iniciado sesión y tiene los permisos necesarios
/* if (!isset($_SESSION['cuil']) || $_SESSION['rol'] == '1') {
    
    // Genera el código JavaScript para mostrar la alerta y redirigir
    echo '<script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>';
    echo '<script>
        Swal.fire({
            icon: "error",
            title: "Acceso denegado",
            text: "No tienes permisos para acceder.",
            confirmButtonText: "Iniciar sesión"
        }).then((result) => {
            if (result.isConfirmed) {
                window.location.href = "/login.php";
            }
        });
    </script>';
    exit();
}
  */
include "../header.php";
include "../footer.php";
?>
<!-- Incrustar las variables de sesión en un div oculto -->
<div id="sessionData" style="display: none;" data-id_usuario="<?php echo $id_usuario; ?>"></div>
<!-- <link rel="stylesheet" href="../public/css/tablas.css"> -->
<head>
<link rel="stylesheet" href="../public/css/ver_recibo.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
<style>
    .info-icon {
        margin-left: 10px;
        color: #007bff;
        font-size: 16px;
        cursor: pointer;
        opacity: 0.7;
    }
    .info-icon:hover {
        opacity: 1;
    }
    .info-icon:hover .tooltip {
        visibility: visible;
        opacity: 1;
    }
    .tooltip {
        visibility: hidden;
        width: auto;
        background-color: #333;
        color: #fff;
        text-align: center;
        border-radius: 5px;
        padding: 5px;
        position: absolute;
        z-index: 1;
        top: -5px;
        left: 110%;
        opacity: 0;
        transition: opacity 0.3s;
        font-size: 12px;
        white-space: nowrap;
    }
</style>
<body> 
<select id="periodo" class="filter-select">
    <option value="">Seleccione Periodo</option>
</select>
    <br/><br/>   
    
   


    <table class="table table-sm dt-responsive nowrap"  id="tablaRecibosDataTable">
        <thead>            
            <th>Recibo</th>
            <th>Periodo</th>  
            <th>Acciones</th>
        </thead>
        <tbody>  
        </tbody>
    </table>   

<script src="../public/js/recibos/recibos.js"></script>

<script>
    var id_usuario = <?php echo json_encode($id_usuario); ?>;
    var cuil = <?php echo json_encode($cuil); ?>;
    $(document).ready(function() {
    // Llamar a la función para cargar los periodos al cargar la página
    cargarPeriodos(id_usuario,cuil);
});
        $(document).ready(function(){
    // Pasar el id_usuario a la función cargarTablaRecibos
    var id_usuario = <?php echo json_encode($id_usuario); ?>;
    var cuil = <?php echo json_encode($cuil); ?>;
    /* console.log('id:'+id_usuario); */
    // Llamar cargarTablaRecibos con el periodo inicial (vacío)
    /* cargarTablaRecibos(id_usuario, ''); */
    // Agregar evento change para el select de periodo
    $('#periodo').on('change', function() {
        var periodoSeleccionado = $(this).val();    
        cargarTablaRecibos(id_usuario, periodoSeleccionado,cuil);
    });
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
<div id="pdfContainer" style="display: none;">
    <embed id="pdfEmbed" src="" width="600" height="500" type="application/pdf">
</div></body>
</html>
