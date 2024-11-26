<!DOCTYPE html>
<html lang="es">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="public/css/menu.css">
    <link rel="shortcut icon" href="https://apps.hospitalposadas.gob.ar/intranet/css/hospi/img/logoPOSADAS_color-01.png">    
    <link rel="stylesheet" href="public/bootstrap/bootstrap.min.css">
    <title>Recibos-HNAP | Registro de usuario. </title>
</head>

<body>
    
        <div class="wrapper fadeInDown">
        <div id="formContent">
            <!-- Tabs Titles -->
            <br>
            <!-- Icon -->
            <div class="fadeIn first">
            <img src="public/img/imgMail.png" id="icon" alt="User Icon" />
                <h4>Recibos de sueldo-HNAP</h4>
                <h4>Registro de usuario</h4>
            </div>
            <!-- Formulario de registro -->   
            <form id="formVerificarCorreo" method="POST"  onsubmit="return verificarCorreo()"> 
                    <input type="text" class="fadeIn second" placeholder="Nombre" id="nombre"name="nombre" oninput="javascript: if (this.value.length > this.maxLength) this.value = this.value.slice(0, this.maxLength);" maxlength="20" required>
                    <input type="text" class="fadeIn second" placeholder="Apellido" id="apellido" name="apellido" oninput="javascript: if (this.value.length > this.maxLength) this.value = this.value.slice(0, this.maxLength);" maxlength="20" required>
                    <input type="number" class="fadeIn second" placeholder="Ingrese su número de cuil sin separadores" id="cuil"name="cuil" oninput="javascript: if (this.value.length > this.maxLength) this.value = this.value.slice(0, this.maxLength);" maxlength="11" title="Ingrese su número de cuil sin separadores ( - , / )" required>
                    <input type="email" class="fadeIn second" placeholder="Correo electronico" id="email" name="email" oninput="javascript: if (this.value.length > this.maxLength) this.value = this.value.slice(0, this.maxLength);" maxlength="40" required>
                    <input type="password" class="fadeIn second" placeholder="Contraseña" id="password" name="password" required minlength="8" pattern="(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}" title="La contraseña debe contener al menos 8 caracteres, incluyendo al menos una letra mayúscula, una letra minúscula y un número" oninput="javascript: if (this.value.length > this.maxLength) this.value = this.value.slice(0, this.maxLength);" maxlength="20" required>   
                    <br>        <br>    
                    <button type="submit" id="botonRegistrar" class="btn btn-primary">Registrar</button>
                    <br><br>
            </form>   
          
            <!-- VOLVER AL INDEX -->
            <div id="formFooter">
                <a class="underlineHover" href="index.html">Volver</a>
            </div>
           
        </div>
    </div>




    <script src="public/jquery/jquery-3.6.0.min.js"></script>
    <script src="public/bootstrap/popper.min.js"></script>
    <script src="public/bootstrap/bootstrap.min.js"></script><!-- 
    <script src="public/sweetalert2/sweetalert2@11.js"></script> -->
    <script src="public/js/usuarios/verificarCorreo.js"></script>

</body>
</html>