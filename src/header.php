<?
if (session_status() == PHP_SESSION_NONE) {
    session_start();
}
?>

<!DOCTYPE html>
<html lang="es"> 

<head>
<meta charset="UTF-8" />
<meta http-equiv="X-UA-Compatible" content="IE=edge" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<link rel="shortcut icon" href="https://apps.hospitalposadas.gob.ar/intranet/css/hospi/img/logoPOSADAS_color-01.png" />
<!-- carga el estilo a la tabla -->
<link rel="stylesheet" href="../public/css/Style.css" /> 
<link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.11.5/css/jquery.dataTables.css">


 <link rel="stylesheet" href="../public/bootstrap/bootstrap.min.css" />
<link rel="stylesheet" href = '../public/datatable/dataTables.bootstrap4.min.css'>
<link rel="stylesheet" href = '../public/datatable/responsive.bootstrap4.min.css'> 

<!-- Agregado 11/06 -->
<link rel="stylesheet" href="https://cdn.datatables.net/1.11.5/css/jquery.dataTables.min.css">
<link rel="stylesheet" href="https://cdn.datatables.net/buttons/2.2.2/css/buttons.dataTables.min.css">
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">  <!-- Carga estilos -->
<!-- Agregado 11/06 -->

<!-- Agregado 16/08 carteleria de ajax -->
 <!-- SweetAlert2 CDN -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/sweetalert2@11/dist/sweetalert2.min.css">
<script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>

    <title>Recibos-HNAP | Inicio </title>

    <title>Tabla de Archivos PDF</title>

    
<div class="container">
        <div class="navbar">
            <img src="../public/img/logo.png" style="margin:3vh;margin-top:  0;" class="logo" alt="Main Logo">
        

            <ul>
            <?php if (isset($_SESSION['cuil']) && ($_SESSION['rol'] == 1)or($_SESSION['rol'] == 2)or($_SESSION['rol'] == 3)): ?>
            <li><a href="misDatos.php">Mis datos</a></li>
            <li><a href="tablaRecibos.php">Recibos</a></li>
        <?php endif; ?>

        <?php if (isset($_SESSION['cuil']) && $_SESSION['rol'] == 2): ?>
            <li><a href="abmusuarios.php">Usuarios</a></li>
            <?php endif; ?>
        <?php if (isset($_SESSION['cuil']) && (($_SESSION['rol'] == 3)or($_SESSION['rol'] == 2))): ?>
            <li><a href="carga.php">Carga</a></li>
            <?php endif; ?>
            <?php if (isset($_SESSION['cuil']) && $_SESSION['rol'] == 2): ?>
                <li><a href="Activacion.php">Activar</a></li>
        <?php endif; ?>
            <li><a href="" id="logout">Cierre de sesión</a></li>
            </ul>
        </div>    

   
        <script>
document.getElementById('logout').addEventListener('click', function(event) {
    event.preventDefault();
    Swal.fire({
        title: 'Cerar sesión',
        text: "¿Usted desea cerrar la sesión?",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Sí, cerrar sesión'
    }).then((result) => {
        if (result.isConfirmed) {
            window.location.href = '../index.php';
        }
    });
});
</script>