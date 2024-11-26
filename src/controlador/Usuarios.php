<?php
    include "Conexion.php";
    //include "mailRegistro2.php";    
   // include "mailRestablecerContrasenia.php";   
    use PHPMailer\PHPMailer\PHPMailer;
    use PHPMailer\PHPMailer\Exception;
    require 'PHPMailer/src/Exception.php';
    require 'PHPMailer/src/PHPMailer.php';
    require 'PHPMailer/src/SMTP.php';     
    
        class Usuarios extends Conexion{
//Agregar nuevo usuario (recibo de sueldo chekeado)**********  
        function agregaNuevoUsuario($cuil,$nombre,$apellido,$rol,$legajo,$email) {               
                //$passwordh = password_hash($password, PASSWORD_BCRYPT);
                $conexion = Conexion::conectar();
                //consulto si existe el usuario
                $sql1= "SELECT * from usuarios"; 
                $respuesta1 = mysqli_query($conexion, $sql1);
                while($row = mysqli_fetch_array($respuesta1))                             
                        {
                            $cuil_db=$row['cuil'];                            
                            $legajo_db=$row['legajo'];
                            $email_db=$row['email'];                              
                            if($cuil==$cuil_db)
                            {
                                //retorno de error cuil
                                return "cuilError";
                            }
                            /* else if($legajo_db==$legajo){
                                //retorno de error cuil
                                return "legajoError";
                            } */
                            else if($email_db==$email)
                            {
                                //retorno de error cuil
                                return "emailError";
                            }
                        }
                        //fin while 
                            //inserto en la base de datos los datos del formulario
                            /* $caracteresPermitidos = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ';
                            $codigo=substr(str_shuffle($caracteresPermitidos), 0, 4);//genera un codigo al azar */
                            $codigo = rand(100000, 999999);
                            $habilitado=1;
                            $validacionCorreo=0;
                            $primer_ingreso=1;
                            $rol=1;
                            $sql = "INSERT INTO usuarios (cuil, nombre, apellido, rol, legajo, email,validacionCorreo,pass,habilitado,primer_ingreso) 
                            VALUES ('$cuil', '$nombre', '$apellido', '$rol', '$legajo', '$email','$validacionCorreo','$codigo',$habilitado,'$primer_ingreso')";  
                            mysqli_query($conexion, $sql); //conexion a la base de datos
                            //return $sql;                                
                                    //debe enviar correo electronico 
                                    $mail = new PHPMailer(true);
                                    try {                                        
                                            $mail->SMTPDebug = 0;
                                            $mail->isSMTP();
                                            $mail->Host = 'mail.hospitalposadas.gob.ar';
                                            $mail->SMTPAuth = true;
                                            $mail->Username = 'reciboshnap@hospitalposadas.gob.ar';//cambiar el correo por el nuevo
                                            $mail->Password = 'Hn4pr3cib0s';//poner la contraseña del nuevo correo
                                            $mail->SMTPSecure = 'ssl';
                                            $mail->Port = 465;
                        $mail->SMTPOptions = array (
    'ssl' => array (
        'verify_peer' => false,
        'verify_peer_name' => false,
        'allow_self_signed' => true
    )
);  
					    $mail->CharSet = 'UTF-8';
                                            $mail->setFrom('reciboshnap@hospitalposadas.gob.ar', 'Sistema de recibos de sueldo');
                                            $mail->addAddress($email);
                                            $mail->isHTML(true);
                                            $mail->Subject = 'Primer ingreso sistema de recibos de sueldo';
                                            $mail->Body = '
                                                <!DOCTYPE html>
                                                <html lang="es">
                                                <head>
                                                    <meta charset="UTF-8">
                                                    <meta http-equiv="X-UA-Compatible" content="IE=edge">
                                                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                                                    <title>Sistema de recibos de sueldos</title>
                                                </head>
                                                <body>                                   
                                                    <div class="row">                                
                                                        <img style="width:50px; height:50px;" src="https://comdis.hospitalposadas.gob.ar/public/img/imgMail.png">                                
                                                        <h1>Bienvenido/a a sistema de recibos de sueldos de Hospital Nacional Prof. Alejandro Posadas:</h1> 
                                                        <h3>Usted ha sido dado de alta en el sistema de recibos de sueldos del Hospital Posadas. Por única vez, se generó una contraseña temporal para su primer ingreso.</h3>                                
                                                    </div>
                                                    <h3>Contraseña temporal '.$codigo.'</h3>                                            
                                                </body>
                                                </html>';
                                            $mail->send();     
                                            return 1;
                                        }
                                        catch (Exception $e) {
                                        return 0;
                                        }                                                                   
                        //fin del filtro si no esta repetido legajo email y cuil               
            }  //fin funcion   
                        

            //carga tabla usuario (recibo de sueldo chekeado)**********
            public function cargaTablaUsuarios() {
                // Crear una instancia de la clase Conexion
                $conexion = new Conexion();
                // Obtener la conexión utilizando el método conectar()
                $conn = $conexion->conectar();  
                $sql = "SELECT id_usuario,cuil, nombre, apellido, legajo, email, rol FROM usuarios WHERE habilitado = '1'";  
                // Ejecutar consulta
                $query = $conn->query($sql);  
                // Preparar datos para la respuesta
                $data = array();
                while ($row = $query->fetch_assoc()) {
                    $data[] = $row;
                }    
                // Crear respuesta en formato JSON
                $response = array(
                    //"draw" => intval($_POST['draw']), // Número de petición (es igual al número de peticiones hechas)
                    "recordsTotal" => count($data), // Total de registros sin ningún filtro
                    "recordsFiltered" => count($data), // Total de registros con el filtro aplicado (en este caso, no hay filtro)
                    "data" => $data // Datos a mostrar en la tabla
                );                
                // Enviar respuesta
                echo json_encode($response); 
            }

            //Deshabilitar usuario (recibo de sueldo chekeado)**********
            public function deshabilitarUsuario($id_usuario)
            {                                    
            $conexion = Conexion::conectar();
            $sql = "UPDATE usuarios set habilitado = '0' where id_usuario='$id_usuario'";          
            mysqli_query($conexion, $sql); 
                return 1;
            }

        public function loginUsuario($cuil, $password){
            session_destroy();                
            $conexion = Conexion::conectar();
            $sql = "SELECT * FROM usuarios
                    WHERE cuil = '$cuil'";
            $respuesta = mysqli_query($conexion, $sql);               
            while($row = mysqli_fetch_array($respuesta))                             
                        {
                            $cuil_db=$row['cuil'];
                            $correo_db=$row['email'];
                            $validacionCorreo_db=$row['validacionCorreo'];
                            $password_db=$row['pass'];
                            $rol=$row['rol'];
                            $nombre_db=$row['nombre'];
                            $apellido_db=$row['apellido'];
                            $habilitado_db=$row['habilitado'];
                            $id_usuario_db=$row['id_usuario'];
                            $legajo_db=$row['legajo'];
                            $proceso_cambio_pass_db=$row['proceso_cambio_pass'];
                            $primer_ingreso_db=$row['primer_ingreso'];
                        }
                        //verifica 
                        /*  if(password_verify($password,$password_db)) */
                        if ($password==$password_db)
                        { 
                            $bandera_pass=1;
                        }
                        else{
                            $bandera_pass=0;
                        }   
            if(($cuil==$cuil_db)and($bandera_pass==1)and($habilitado_db==1))
            {                
            session_start();
                $_SESSION['cuil']=$cuil_db;
                $_SESSION['rol']=$rol;  
                $_SESSION['nombre']=$nombre_db; 
                $_SESSION['apellido']=$apellido_db;
                $_SESSION['id_usuario']=$id_usuario_db;
                $_SESSION['legajo']=$legajo_db;
                $_SESSION['tiempo'] = time();
                //aca realiza un registro de logeo en logins
                $conexion = Conexion::conectar();
                $sql = "INSERT INTO `logins`(`usuario`,                          
                `id_usuario`) VALUES ('$cuil_db',
                '$id_usuario_db') ";
                mysqli_query($conexion, $sql);
                        //verificacion de correo electronico
                        //  ES PRIMER INGRESO???
                        if($primer_ingreso_db==1)
                        {
                            return 5;
                        }

                        //TIENE CORREO?
                        if(($correo_db!=null)or($correo_db!=""))
                        {  //SI
                               //ESTA VALIDADO??
                            if($validacionCorreo_db==1){
                                //SI  
                                //pregunta si tiene proceso de cambio de contraeña activo

                                if(($cuil==$cuil)and($bandera_pass==1)and($habilitado_db==1)and($proceso_cambio_pass_db==1))
                                {
                                    //$tipo_error="Usuario usuario con proceso de cambio de contraseña abierto, por favor termine el proceso revisando su correo electronico.";
                                    //Usuarios::login_fallido($cuil,$password,$tipo_error);                    
                                    return 4;
                                } else {

                                    return 1;
                                } 
                            }
                                //correcto devuelve 1 inicia sesion
                                else if($validacionCorreo_db==0){                                
                                        return 2; //cartel "usted debe validar su correo electornico"
                                }                          

                        }
                        else if((isset($correo_db))or($correo_db==""))
                        {
                            return 3;//Declaracion de correo electronico

                        }                                      
            }
            //usuario deshabilitado
            else if(($cuil==$cuil_db)and($bandera_pass==1)and($habilitado_db==0))
            {
                $tipo_error="Usuario deshabilitado";
                Usuarios::login_fallido($cuil,$password,$tipo_error);
                return 50;
            }
            //usuario pendiente de aprobacion debera esperar ser notificado por correo electronico cuando su usuario sea aprobado en el sistema.           
        /*  else if($cuil=="developer")                 
            {
                $tipo_error="Usuario developer";
                Usuarios::login_fallido($cuil,$password,$tipo_error);
                $quedeveloper=100;
                return $quedeveloper;
            } */
            //usuario o contraseñas incorrectos 
            else 
            {   
                $tipo_error="Usuario o contraseñas incorrectos ";                                   
                $retorno= Usuarios::login_fallido($cuil,$password,$tipo_error);                       
                return 0;
            }  
        }    

//corre la funcion login fallido 
            function login_fallido($cuil,$password,$tipo_error)
            {
                $conexion = Conexion::conectar();                    
                $ip_adress = $_SERVER['REMOTE_ADDR'];                    
                $user_agent = $_SERVER['HTTP_USER_AGENT'];
                $host_name = $_SERVER['HTTP_HOST'];
                if (strpos($user_agent, 'Opera') !== false || strpos($user_agent, 'OPR') !== false) {
                    $navegador = 'Opera';
                } elseif (strpos($user_agent, 'Chrome') !== false) {
                    $navegador = 'Google Chrome';
                } elseif (strpos($user_agent, 'Firefox') !== false) {
                    $navegador = 'Mozilla Firefox';
                } elseif (strpos($user_agent, 'Edge') !== false) {
                    $navegador = 'Microsoft Edge';
                } elseif (strpos($user_agent, 'Safari') !== false && strpos($user_agent, 'Chrome') === false) {
                    $navegador = 'Safari';
                } else {
                    $navegador = 'Otro navegador';
                }
                //guarda la geolocalizacion obtenida por una api                
                $token = '5b5c1330a20d77'; // Reemplaza con tu token de acceso de ipinfo.io
                $url = "http://ipinfo.io/$ip_adress/json?token=$token";                    
                $response = file_get_contents($url);
                if($response !== false) {
                    // La solicitud fue exitosa, $response contiene el JSON
                    $data = json_decode($response);
                    // Ahora puedes trabajar con los datos decodificados en $data
                } else {
                    // Ocurrió un error al hacer la solicitud
                    echo "Error al obtener el JSON desde la URL";
                }             
                if ($data !== null && isset($data->city) && isset($data->country)) {
                    $city = $data->city;
                    $country = $data->country;
                    $latitude = $data->loc ? explode(',', $data->loc)[0] : '';
                    $longitude = $data->loc ? explode(',', $data->loc)[1] : '';
                    $googleMapsLink = "https://www.google.com/maps?q=$latitude,$longitude";
                    $escapedGoogleMapsLink = mysqli_real_escape_string($conexion, $googleMapsLink); // Escapar la cadena
                
                    // Registrar en la base de datos
                    $sql = "INSERT INTO `t_logins_fallidos`(`usuario`, `pass`, `navegador`, `ip_adress`, `tipo_error`, `host_name`, `google_maps`) 
                            VALUES ('$cuil', '$password', '$navegador', '$ip_adress', '$tipo_error', '$host_name', '$escapedGoogleMapsLink')";
                    mysqli_query($conexion, $sql);
                } else {
                    $googleMapsLink = "Error al obtener la información de geolocalización.";
                
                    // Registrar en la base de datos con el mensaje de error
                    $sql = "INSERT INTO `logins_fallidos`(`usuario`, `pass`, `navegador`, `ip_adress`, `tipo_error`, `host_name`, `google_maps`) 
                            VALUES ('$cuil', '$password', '$navegador', '$ip_adress', '$tipo_error', '$host_name', '$googleMapsLink')";
                    mysqli_query($conexion, $sql);
                }
                
            }

//FUNCION MIS DATOS
                function misDatos($id_usuario) { 
                    // Crear una instancia de la clase Conexion
                    $conexion = new Conexion();
                    // Obtener la conexión utilizando el método conectar()
                    $conn = $conexion->conectar();
                    
                    // Consulta para obtener los datos del usuario específico
                    $sql = "SELECT id_usuario, cuil, nombre, apellido, legajo, email FROM usuarios WHERE id_usuario = ?";
                    
                    // Preparar la consulta
                    $stmt = $conn->prepare($sql);
                    $stmt->bind_param("i", $id_usuario); // "i" indica que el parámetro es un entero
                    
                    // Ejecutar la consulta
                    if ($stmt->execute()) {
                        // Obtener el resultado
                        $result = $stmt->get_result();
                        if ($result->num_rows > 0) {
                            // Obtener los datos del usuario
                            $userData = $result->fetch_assoc();
                            
                            // Crear respuesta en formato JSON
                            $response = array(
                                'id_usuarioMisDatos' => $userData['id_usuario'],
                                'cuilMisDatos' => $userData['cuil'],
                                'nombreMisDatos' => $userData['nombre'],
                                'apellidoMisDatos' => $userData['apellido'],
                                'legajoMisDatos' => $userData['legajo'],
                                'emailMisDatos' => $userData['email']
                            );                            
                            // Enviar respuesta JSON                           
                            echo json_encode($response);
                        } else {
                            echo json_encode(array('error' => 'No se encontraron datos para el usuario especificado.'));
                        }
                    } else {
                        echo json_encode(array('error' => 'Error al ejecutar la consulta.'));
                    }
                    
                    // Cerrar la declaración y la conexión
                    $stmt->close();
                    $conn->close();
                }  

                function declaracionCorreo($id_usuario, $cuil, $email, $email2) {        
                    if ($email == $email2) {   
                        $conexion = new Conexion();  
                        $conn = $conexion->conectar();                        
                        // Verificar si el correo ya está registrado
                        $sql1 = "SELECT email FROM usuarios WHERE email = ?";
                        $stmt1 = $conn->prepare($sql1);
                        $stmt1->bind_param("s", $email);
                        $stmt1->execute();
                        $stmt1->store_result();                        
                        if ($stmt1->num_rows > 0) {
                            $stmt1->close();
                            $conn->close();
                            return 6; // el correo se encuentra ingresado
                        } else {
                                // Consulta SQL
                                $codigo = rand(100000, 999999);
                                    $sql = "UPDATE usuarios SET email = ?, validacionCorreo = 0, codigo_validacion_correo = ? WHERE cuil = ? AND id_usuario = ?";
                                    $stmt2 = $conn->prepare($sql);
                                    $stmt2->bind_param("ssss", $email, $codigo, $cuil, $id_usuario);
                                if ($stmt2->execute()) {
                                    $stmt2->close();
                                    
                                    $mail = new PHPMailer(true);
                                    try {                                        
                                        $mail->SMTPDebug = 0;
                                        $mail->isSMTP();
                                        $mail->Host = 'mail.hospitalposadas.gob.ar';
                                        $mail->SMTPAuth = true;
                                        $mail->Username = 'reciboshnap@hospitalposadas.gob.ar';//cambiar el correo por el nuevo
                                        $mail->Password = 'Hn4pr3cib0s';//poner la contraseña del nuevo correo
                                        $mail->SMTPSecure = 'ssl';
                                        $mail->Port = 465;
                        $mail->SMTPOptions = array (
    'ssl' => array (
        'verify_peer' => false,
        'verify_peer_name' => false,
        'allow_self_signed' => true
    )
);    
					$mail->CharSet = 'UTF-8';
                                        $mail->setFrom('reciboshnap@hospitalposadas.gob.ar', 'Sistema de recibos de sueldo');
                                        $mail->addAddress($email);
                                        $mail->isHTML(true);
                                        $mail->Subject = 'Declaracion de correo electrónico';
                                        $mail->Body = '
                                            <!DOCTYPE html>
                                            <html lang="es">
                                            <head>
                                                <meta charset="UTF-8">
                                                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                                                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                                                <title>Sistema de recibos de sueldos</title>
                                            </head>
                                            <body>                                   
                                                <div class="row">                                
                                                    <img style="width:50px; height:50px;" src="https://comdis.hospitalposadas.gob.ar/public/img/imgMail.png">                                
                                                    <h1>Bienvenido/a a sistema de recibos de sueldos:</h1> 
                                                    <h3>Tu correo electrónico ya ha sido registrado y asociado a tu usuario. Solo queda validarlo ingresando el código de verificación</h3>                                
                                                </div>
                                                <h3>Su código de verificación es: '.$codigo.'</h3>                                            
                                            </body>
                                            </html>';
                                        $mail->send();                                        
                                        // Aquí puedes agregar la lógica para crear un usuario automáticamente si es necesario.                                        
                                        $conn->close();
                                        return 1;
                                    } catch (Exception $e) {
                                    $conn->close();
                                        return 0;
                                /*  $errorInfo = $mail->ErrorInfo;
                                    $devuelve = error_log("Error al enviar el correo: $errorInfo");
                                    $conn->close();
                                    return $devuelve; */
                                    }
                                } else {
                                    $stmt2->close();
                                    $conn->close();
                                    return 0; // Fallo en la actualización de la base de datos
                                }
                        }   
                    } else {
                        return 2; // Los correos no coinciden
                    }
                }
            



            
            function validacionCorreo($id_usuario,$cuil,$codigo)
            {
                $conexion = new Conexion();  
                $conn = $conexion->conectar();                
                // Verificar si el correo ya está registrado y obtener el código de validación
                $sql = "SELECT codigo_validacion_correo FROM usuarios WHERE id_usuario = '$id_usuario'";
                $stmt = $conn->prepare($sql);
                //$stmt->bind_param("ss", $email, $id_usuario);
                $stmt->execute();
                $stmt->store_result();                
                if ($stmt->num_rows > 0) {
                    $stmt->bind_result($codigo_db);
                    $stmt->fetch();            
                    if ($codigo == $codigo_db) {
                                // Códigos coinciden
                                $sql2 = "UPDATE usuarios SET validacionCorreo = 1 WHERE cuil = ? AND id_usuario = ?";
                                $stmt2 = $conn->prepare($sql2);
                                $stmt2->bind_param("ss", $cuil, $id_usuario);
                                if ($stmt2->execute()) {
                                $stmt->close();
                                $conn->close();
                                return 1; // Código de validación correcto
                                }
                    } else {
                                // Códigos no coinciden
                                $stmt->close();
                                $conn->close();
                                return 0; // Código de validación incorrecto
                    }
                } else {
                    // No se encontró el usuario
                    $stmt->close();
                    $conn->close();
                    return $sql; // Usuario no encontrado
                }
            }   

        ///falta terminar
        function resetPassword($id_usuario) {       
            $conexion = new Conexion();  
            $conn = $conexion->conectar();                        
            // Verificar si el correo ya está registrado
            $sql1 = "SELECT email,validacionCorreo,proceso_cambio_pass FROM usuarios WHERE id_usuario = ?";
            $stmt1 = $conn->prepare($sql1);
            $stmt1->bind_param("s", $id_usuario);
            $stmt1->execute();
            $stmt1->store_result();       

            if ($stmt1->num_rows > 0) {
                // Vincular los resultados a variables
                $stmt1->bind_result($email, $validacionCorreo, $proceso_cambio_pass);
                $stmt1->fetch();
                
                // Evaluar el valor de proceso_cambio_pass y validacionCorreo
                if ($proceso_cambio_pass == 1) {
                    return 0;//proceso de cambio de contraseña en proceso
                }
                else if($validacionCorreo==0)
                {
                return 2;//correo electronico no validado 
                }

                else if(($email=="")or($email==null))
                {
                return 3;//no posee correo electronico
                }

                else {
                    // Consulta SQL
                    $pass_temporal = rand(100000, 999999);
                        $sql = "UPDATE usuarios SET pass = ?, proceso_cambio_pass = 1 WHERE id_usuario = ?";
                        $stmt2 = $conn->prepare($sql);
                        $stmt2->bind_param("ss", $pass_temporal,$id_usuario);
                    if ($stmt2->execute()) {
                                                $stmt2->close();                            
                                                $mail = new PHPMailer(true);
                                                try {                                
                                                    $mail->SMTPDebug = 0;
                                                    $mail->isSMTP();
                                                    $mail->Host = 'mail.hospitalposadas.gob.ar';
                                                    $mail->SMTPAuth = true;
                                                    $mail->Username = 'reciboshnap@hospitalposadas.gob.ar';//cambiar el correo por el nuevo
                                                    $mail->Password = 'Hn4pr3cib0s';//poner la contraseña del nuevo correo
                                                    $mail->SMTPSecure = 'ssl';
                        $mail->Port = 465;
                    $mail->SMTPOptions = array (
'ssl' => array (
    'verify_peer' => false,
    'verify_peer_name' => false,
    'allow_self_signed' => true
)
);  
                                                    $mail->CharSet = 'UTF-8';
                                                    $mail->setFrom('reciboshnap@hospitalposadas.gob.ar', 'Sistema de recibos de sueldo');
                                                    $mail->addAddress($email);
                                                    $mail->isHTML(true);
                                                    $mail->Subject = 'Declaracion de correo electrónico';
                                                    $mail->Body = '
                                                        <!DOCTYPE html>
                                                        <html lang="es">
                                                        <head>
                                                            <meta charset="UTF-8">
                                                            <meta http-equiv="X-UA-Compatible" content="IE=edge">
                                                            <meta name="viewport" content="width=device-width, initial-scale=1.0">
                                                            <title>Sistema de recibos de sueldo</title>
                                                        </head>
                                                        <body>                                   
                                                            <div class="row">                                
                                                                <img style="width:50px; height:50px;" src="https://comdis.hospitalposadas.gob.ar/public/img/imgMail.png">                                
                                                                <h1>Bienvenido/a a sistema de recibos de sueldos:</h1> 
                                                                <h3>Se solicitó el restablecimiento de tu contraseña. Te proporcionaremos una contraseña temporal, luego deberás ingresar una nueva.</h3>                                
                                                            </div>
                                                            <h3>Su contraseña temporal es: '.$pass_temporal.'</h3>                                            
                                                        </body>
                                                        </html>';
                                                    $mail->send();                                        
                                                    // Aquí puedes agregar la lógica para crear un usuario automáticamente si es necesario.                                        
                                                    $conn->close();
                                                    return 1;
                                                } catch (Exception $e) {
                                                    $conn->close();
                                                    return 0;
                                                }
                                            }   
                                            else{
                                                return 0;
                                            }
                    }
        }
        return 0;
                
            } 

//funcion nuevo pass                 
                        function nuevoPass($pass, $pass2, $id_usuario)
                        {
                            if ($pass == $pass2) {
                                $conexion = new Conexion();
                                $conn = $conexion->conectar();
                                //pregunta si es primer ingreso 
                                $sql1= "SELECT primer_ingreso from usuarios where id_usuario='$id_usuario'"; 
                                $respuesta1 = mysqli_query($conn, $sql1);
                                while($row = mysqli_fetch_array($respuesta1))                             
                                        {
                                            $primer_ingreso_db=$row['primer_ingreso'];                                             
                                        }                                        
                                        //si es primer ingreso VALIDA CORREO y PONE PRIMER INGRESO EN 0 TODO en una sola accion
                                            if($primer_ingreso_db==1)
                                            {
                                                    // Consulta SQL
                                                    $sql = "UPDATE usuarios SET pass = ?, proceso_cambio_pass = 0,primer_ingreso = 0,validacionCorreo=1 WHERE id_usuario = ?";                                               
                                                    $stmt2 = $conn->prepare($sql);
                                                    $stmt2->bind_param("ss", $pass, $id_usuario);
                                                    if ($stmt2->execute()) {
                                                        $stmt2->close();
                                                        $conn->close();
                                                        // Reemplazar los parámetros en la consulta
                                                        $query = $sql;
                                                        $query = preg_replace('/\?/', "'$pass'", $query, 1);
                                                        $query = preg_replace('/\?/', "'$id_usuario'", $query, 1);                                                        
                                                        return 1;
                                                    } else {
                                                        return 0; // Fallo en la actualización de la base de datos
                                                    }
                                            }
                                            else{   
                                                //si no es primer ingreso realiza un reseteo de conntraseña comun y corriente
                                                // Consulta SQL
                                                $sql = "UPDATE usuarios SET pass = ?, proceso_cambio_pass = 0 WHERE id_usuario = ?";
                                                $stmt2 = $conn->prepare($sql);
                                                $stmt2->bind_param("ss", $pass, $id_usuario);
                                                if ($stmt2->execute()) {
                                                    $stmt2->close();
                                                    $conn->close();
                                                    // Reemplazar los parámetros en la consulta
                                                    $query = $sql;
                                                    $query = preg_replace('/\?/', "'$pass'", $query, 1);
                                                    $query = preg_replace('/\?/', "'$id_usuario'", $query, 1);
                                                    
                                                    return 1;
                                                } else {
                                                    return 0; // Fallo en la actualización de la base de datos
                                                }

                                            }
                            } else {
                                return 2; // Las contraseñas no coinciden validación por back
                            }
                        }

//Actualizar Usuario

 function  editarUsuario($id_usuario,$cuil,$nombre,$apellido,$legajo,$email,$rol){  
    $conexion=Conexion::conectar();
    $sql_actualizarUsuario = "SELECT * FROM usuarios
    WHERE id_usuario = '$id_usuario'";
    $respuesta_actualizarUsuario = mysqli_query($conexion,$sql_actualizarUsuario);
    while($row = mysqli_fetch_array($respuesta_actualizarUsuario)){
        $cuil_db=$row['cuil'];
        $nombre_db=$row['nombre'];
        $apellido_db=$row['apellido'];
        $legajo_db=$row['legajo'];
        $email_db=$row['email'];
        $rol_db=$row['rol'];   
        $proceso_cambio_pass_db=$row['proceso_cambio_pass']; 
    }   
    //ASI NO DARIO!!!!
  /*   if (empty($email_db) || $email_db === null || $email !== $email_db) {
        $validacionCorreo = 1 && $proceso_cambio_pass_db = 0;
    }
    
   /*  if ($email !== $email_db && $proceso_cambio_pass_db == 1) {
       
    }  */
 
//ASI SI :)
    if(($email_db=="")or($email_db==null)or($email!=$email_db))
    {
        $validacionCorreo=1;
    }
    if(($email!=$email_db)and($proceso_cambio_pass_db==1)){
        $proceso_cambio_pass=0;
    }
    if(($cuil!=$cuil_db)
    or($nombre!=$nombre_db)
    or($apellido!=$apellido_db)
    or($legajo!=$legajo_db)
    or($email!=$email_db)
    or($rol!=$rol_db))            
        {               
            
                    //antes de guardar verifica cuil, correo y legajo 
                    // Verificar si el CUIL ya existe

                    
                    $sql_verificarCuil = "SELECT id_usuario FROM usuarios WHERE cuil = '$cuil' AND id_usuario != '$id_usuario'";
                    $resultadoCuil = mysqli_query($conexion, $sql_verificarCuil);                   
                    if (mysqli_num_rows($resultadoCuil) > 0) {
                        mysqli_close($conexion); // Cerrar la conexión antes de retornar
                        return 3;
                    }
                    // Verificar si el legajo ya existe
                    $sql_verificarLegajo = "SELECT id_usuario FROM usuarios WHERE legajo = '$legajo' AND id_usuario != '$id_usuario'";
                    $resultadoLegajo = mysqli_query($conexion, $sql_verificarLegajo);
                    if (mysqli_num_rows($resultadoLegajo) > 0) {
                        mysqli_close($conexion); // Cerrar la conexión antes de retornar
                        return 4;
                    }
                    // Verificar si el correo ya existe
                    $sql_verificarCorreo = "SELECT id_usuario FROM usuarios WHERE email = '$email' AND id_usuario != '$id_usuario'";
                    $resultadoCorreo = mysqli_query($conexion, $sql_verificarCorreo);
                    if (mysqli_num_rows($resultadoCorreo) > 0) {
                        mysqli_close($conexion); // Cerrar la conexión antes de retornar
                        return 5;
                    }else{ 
                        
                        //si el correo esta vacio ingresa un correo YA VALIDADO.
                        if($validacionCorreo==1)
                        {
                            $proceso_cambio_pass=0;
                            $sql="UPDATE `usuarios` SET
                            `cuil`='$cuil',
                            `nombre`='$nombre',
                            `apellido`='$apellido',
                            `rol`='$rol',
                            `legajo`='$legajo',           
                            `email`='$email',
                            `validacionCorreo`='$validacionCorreo',
                            `proceso_cambio_pass`='$proceso_cambio_pass'
                            WHERE id_usuario = '$id_usuario'";                                                 
                                mysqli_query($conexion, $sql);  
                                mysqli_close($conexion);  
                                return 1;

                        }
                        //Si ya tenia correo validado solamente cambia el correo.
                        else{
                            $proceso_cambio_pass=0;
                            $sql="UPDATE `usuarios` SET
                            `cuil`='$cuil',
                            `nombre`='$nombre',
                            `apellido`='$apellido',
                            `rol`='$rol',
                            `legajo`='$legajo',           
                            `email`='$email',
                            `proceso_cambio_pass`='$proceso_cambio_pass'
                            WHERE id_usuario = '$id_usuario'";                                           
                                mysqli_query($conexion, $sql);  
                                mysqli_close($conexion);  
                                return 1;

                        }                                      
                        }
                    }
                        else
                        {
                            return 2;
                        }                        
       // $dni_db=$row["dni_madre"];                        
}

            }//cerrar la clase
            
