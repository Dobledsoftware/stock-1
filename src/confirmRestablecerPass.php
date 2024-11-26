<?php 


if((isset($_GET['email'])) and (isset($_GET['tokken_pass']) )){
    $email = $_GET['email'] ;
    $tokken_pass= $_GET['tokken_pass'];
   
}else{
    header('Location: ./index.html');
}
?>

<!DOCTYPE html>
<html lang="es">
<head>
    <title>ComDis-HNAP | Restablecer Contraseña.</title>
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="public/css/menu.css">
    <link rel="shortcut icon" href="public/img/PERFIL-intranet-2021.png">
    <link rel="stylesheet" href="public/bootstrap/bootstrap.min.css">
    <title>ComDis-HNAP |  Restablecer Contraseña. </title>
</head>
<body>
    <div class="wrapper fadeInDown">
        <div id="formContent">
            <!-- Tabs Titles -->
            <br>
            <!-- Icon -->
            <div class="fadeIn first">
                <img src="public/img/imgMail.png" id="icon" alt="User Icon" />
                <h4>ComDis-HNAP | Restablecer contraseña.</h4>
            </div>
            <!-- Formulario de verificacion de contraseñas iguales-->  
            <form id="formRestablecerContraseniaConTokken" method="POST"  onsubmit="return restablecerContraseniaConTokken()">                  <br>                
                <input type="password" class="fadeIn second" placeholder="Nueva Contraseña" id="password" name="password" required  minlength="8" pattern="(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}" title="La contraseña debe contener al menos 8 caracteres, incluyendo al menos una letra mayúscula, una letra minúscula y un número"> 
                <br> <br>
               <!-- <input type="password" class="fadeIn second" placeholder="Repita nueva Contraseña" id="password2" name="password2" required> -->
                <input type="password" class="fadeIn second" placeholder="Repita nueva Contraseña" id="password2" name="password2" required minlength="8" pattern="(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}" title="La contraseña debe contener al menos 8 caracteres, incluyendo al menos una letra mayúscula, una letra minúscula y un número">
                <input type="hidden" class="fadeIn second" id="email" name="email" value="<?php echo $email;?>"><br><br>
                <input type="hidden" class="fadeIn second" id="tokken_pass" name="tokken_pass" value="<?php echo $tokken_pass;?>"><br><br>
                <br>
                <input type="submit" class="fadeIn fourth" value="Restablecer Contraseña.">
            </form>            
             <!-- CONTACTE A UN ADMINISTRADOR -->
            <div id="formFooter">
                <a class="underlineHover" href="#" data-toggle="modal" data-target="#modalContacto">Contacte a un administrador</a>
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
    <script src="public/jquery/jquery-3.6.0.min.js"></script>
    <script src="public/bootstrap/popper.min.js"></script>
    <script src="public/bootstrap/bootstrap.min.js"></script>
    <script src="public/sweetalert2/sweetalert2@11.js"></script>
    <script src="public/js/usuarios/restablecerContraseniaConTokken.js"></script>

</body>

</html>






