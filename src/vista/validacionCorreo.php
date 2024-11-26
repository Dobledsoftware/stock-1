<?php 
session_start();
//solo administrador del sistema
        if(isset($_SESSION['cuil'])){
        $cuil = $_SESSION['cuil'];
        $id_usuario = $_SESSION['id_usuario']; // Suponiendo que el id_usuario también está en la sesión
?>
    <script>
        // Guardar los valores de la sesión en sessionStorage de JavaScript
        sessionStorage.setItem('cuil', '<?php echo $cuil; ?>');
        sessionStorage.setItem('id_usuario', '<?php echo $id_usuario; ?>');
        document.addEventListener('DOMContentLoaded', function() {
    // Validación de campos del formulario
  /*   var codigoInput = document.getElementById('codigo');
    if (codigoInput) {
        codigoInput.addEventListener('input', validateCodigo);
        codigoInput.addEventListener('keydown', blockInvalidCodigoCharacters);
    } */
});




document.addEventListener('DOMContentLoaded', function() {

            let codigoInput = document.getElementById('codigo');
            let error = document.getElementById('codigo-error');
            if (codigoInput) {
                codigoInput.addEventListener('input', validateCodigo);
                codigoInput.addEventListener('keydown', blockInvalidCodigoCharacters);
    }


            function validateCodigo() {
                let codigo = codigoInput.value;
                
                if (codigo === '') {
                    error.textContent = '';
                } else if (!/^\d{6}$/.test(codigo)) {
                    error.textContent = 'El código debe tener 6 dígitos.';
                } else {
                    error.textContent = '';
                }
            }
/* 
            codigoInput.addEventListener('input', validateCodigo); */
        });


    function blockInvalidCodigoCharacters(event) {
        if (!/\d/.test(event.key) && !['Backspace', 'Delete', 'ArrowLeft', 'ArrowRight', 'Tab'].includes(event.key)) {
            event.preventDefault();
        }
    }




    </script>
<!DOCTYPE html>
<html lang="es">
<head>
    <title>Recibos de sueldo-HNAP | Validacion</title>
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="../public/css/menu.css">
    <link rel="shortcut icon" href="../public/img/PERFIL-intranet-2021.png">
    <link rel="stylesheet" href="../public/bootstrap/bootstrap.min.css">
    <title>Recibos de sueldo-HNAP | verificación código de seguridad. </title>
</head>
<body>
    <div class="wrapper fadeInDown">
        <div id="formContent">
            <!-- Tabs Titles -->
            <br>
            <!-- Icon -->
            <div class="fadeIn first">
                <img src="../public/img/imgMail.png" id="icon" alt="User Icon" />
                <h4>Recibos de sueldo-HNAP | Validación de correo electrónico.</h4>
            </div>
            <!-- Formulario de verificacion -->
            <form id="formValidacionCorreo" method="POST"  onsubmit="return validacionCorreo()"  >  
                <br>
                <input type="text" class="fadeIn second" id="codigo" name="codigo" placeholder="Código de verificación" oninput="javascript: if (this.value.length > this.maxLength) this.value = this.value.slice(0, this.maxLength);" maxlength="6" required><br>
                <span id="codigo-error" style="color: red; display: none;">El CODIGO debe ser un número de 6 dígitos</span>
                <button type="submit" id="Validar" class="btn btn-primary">Validar</button><br><br>
            </form>              
            <a class="underlineHover" href="../index.php">Volver</a>
            <!-- CONTACTE A UN ADMINISTRADOR -->
            <div id="formFooter">
                <a class="underlineHover" href="#" data-toggle="modal" data-target="#modalContacto">Contáctese con un administrador</a>
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
    <script src="../public/js/usuarios/validacionCorreo.js"></script>
</body>
</html>
<?php

}
?>



