<?php
session_start();
//solo administrador del sistema
        if(isset($_SESSION['cuil'])) {
        $cuil = $_SESSION['cuil'];
        $id_usuario = $_SESSION['id_usuario']; // Suponiendo que el id_usuario también está en la sesión
?>
    <script>
        // Guardar los valores de la sesión en sessionStorage de JavaScript
        sessionStorage.setItem('cuil', '<?php echo $cuil; ?>');
        sessionStorage.setItem('id_usuario', '<?php echo $id_usuario; ?>');
    </script>

<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="../public/css/menu.css">
    <link rel="shortcut icon" href="https://apps.hospitalposadas.gov.ar/intranet/css/hospi/img/logoPOSADAS_color-01.png">
    <link rel="stylesheet" href="../public/bootstrap/bootstrap.min.css">
</head>
<body>
    <div class="wrapper fadeInDown">
        <div id="formContent">
            <!-- Tabs Titles -->
            <br>
            <!-- Icon -->
            <div class="fadeIn first">
            <img src="../public/img/imgMail.png" id="icon" alt="User Icon" />
                <h4>Recibos de sueldo-HNAP | Declaración de correo electrónico. </h4>
            </div>
            <!-- FORMULARIO -->
            <form id="fromdeclaracionCorreo" method="POST" onsubmit="return declaracionCorreo()">
                <br>
                <input type="email" id="email" class="fadeIn second" name="email" placeholder="Correo electronico" oninput="javascript: if (this.value.length > this.maxLength) this.value = this.value.slice(0, this.maxLength);" maxlength="60" required><br>
                <input type="email" id="email2" class="fadeIn second" name="email2" placeholder="Repita su correo electronico" oninput="javascript: if (this.value.length > this.maxLength) this.value = this.value.slice(0, this.maxLength);" maxlength="60" required><br><br>  
                <input type="submit" class="fadeIn fourth" id="Enviar" value="Enviar">
            </form>         
            <!-- VOLVER AL INDEX -->
            <div id="formFooter">
                <a class="underlineHover" href="../index.php">Volver</a>
            </div>            
        </div>
    </div>
    <!-- Modal CONTACTE A UN ADMINISTRADOR-->
    <div class="modal fade" id="modalContacto" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="exampleModalLabel">Contacto</h5>
                    <button type="button" class="close" data-bs-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <div class="modal-body">
                Si tenes alguna dificultad envia un ticket a explicando el problema a: <br><strong>https://apps.hospitalposadas.gob.ar/glpi</strong>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-dismiss="modal">Cerrar</button>
                </div>
            </div>
        </div>
    </div>
    <!--Modal-->
    <script src="../public/jquery/jquery-3.6.0.min.js"></script>
    <script src="../public/bootstrap/popper.min.js"></script>
    <script src="../public/bootstrap/bootstrap.min.js"></script>
    <script src="../public/sweetalert2/sweetalert2@11.js"></script>
    <script src="../public/js/usuarios/declaracionCorreo.js"></script>
</body>
</html>
<?php
}
?>
