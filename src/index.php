<!DOCTYPE html>
<html lang="es">

<head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link rel="stylesheet" href="public/css/menu.css" />
    <!-- <link rel="stylesheet" href="../public/css/carga.css"> -->
    <link rel="shortcut icon"
        href="https://apps.hospitalposadas.gob.ar/intranet/css/hospi/img/logoPOSADAS_color-01.png" />
    <link rel="stylesheet" href="public/bootstrap/bootstrap.min.css" />
    <title>GesRe - HNAP | Inicio</title>
    <!-- Agrega el CDN de Font Awesome -->
    <link rel="stylesheet"
        href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <style>
        .info-icon {
            position: absolute;
            top: 10px;
            right: 10px;
            color: #007bff;
            font-size: 24px;
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
            width: 150px;
            background-color: #333;
            color: #fff;
            text-align: center;
            border-radius: 5px;
            padding: 10px;
            position: absolute;
            z-index: 1;
            top: -35px;
            right: -10px;
            opacity: 0;
            transition: opacity 0.3s;
            font-size: 14px;
            white-space: nowrap;
        }
    </style>
</head>

<body>
    <div class="wrapper fadeInDown" id="login1">
        <div id="formContent">
            <!-- Icono de información -->
            <a href="public/manual/manual.pdf" target="_blank" class="info-icon">
                <i class="fas fa-info-circle"></i>
                <div class="tooltip">Manual de uso</div>
            </a>
            <!-- Tabs Titles -->
            <br />
            <!-- Icon -->
            <div class="fadeIn first">
                <img src="public/img/imgMail.png" id="icon" alt="User Icon" />
                <br /><br />
                <h4>GesRe - HNAP</h4>
                <h4>Inicio de sesión</h4>
            </div>

            <!-- Formulario de logeo -->
            <form id="formLogin" method="POST" onsubmit="return loginUsuario()">
                <br />
                <input type="text" id="cuil" class="fadeIn second" name="cuil" placeholder="Cuil" required
                    maxlength="11" />
                <br />
                <span id="cuil-error" style="color: red; display: none;">El CUIL debe ser un número de 11
                    dígitos</span>

                <input type="password" id="password" class="fadeIn third" name="password" placeholder="Contraseña"
                    required /><br /><br />
                <input type="submit" class="fadeIn fourth" id="submitBtn" value="Ingresar" disabled />
                <p>V 0.1.24</p>
                <p style="font-size:10px;font-style: italic;">Desarrollado por: Departamento de sistemas</p>
                <strong>Hospital Nac. Prof A. Posadas</strong>
            </form>

            <!-- REGISTRARSE lleva al archivo donde están los campos donde registrar los datos ingresados -->
            <div class="container">
                <!-- <a class="underlineHover" href="register.php">Registrarse.</a> -->
            </div>
            <br />
            <!-- CONTACTE A UN ADMINISTRADOR -->
        </div>
    </div>

    <script src="public/jquery/jquery-3.6.0.min.js"></script>
    <script src="public/bootstrap/popper.min.js"></script>
    <script src="public/bootstrap/bootstrap.min.js"></script>
    <script src="public/sweetalert2/sweetalert2@11.js"></script>
    <script src="public/js/usuarios/login.js"></script>
</body>

</html>
