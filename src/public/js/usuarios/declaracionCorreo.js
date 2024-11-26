
function declaracionCorreo() {
    // Obtenemos los valores de los inputs de correo electrónico
    var email = document.getElementById('email').value;
    var email2 = document.getElementById('email2').value;
    // Comprobamos que los correos electrónicos coincidan
    if (email != email2) {
        Swal.fire({
            title: 'Error',
            text: 'Los correos electrónicos no coinciden.',
            icon: 'error',
            allowOutsideClick: false
        });
        return false;
    } //fin if validacion correo por front

    //fin de evaluacion inicia carteles y envio 
    Swal
        .fire({
            title: "Declaración de correo electrónico.",
            text: "¿Usted esta seguro de que los datos ingresados son correctos?",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: "SI",
            cancelButtonText: "NO",
            allowOutsideClick: false
        })
        .then(resultado => {
            if (resultado.value) {
                document.getElementById('Enviar').disabled = true;
                //CARTEL DE CARGANDO
                Swal.fire({
                        title: 'Registrando el correo electrónico.',
                        html: 'Por favor aguarde, se esta procesando su solicitud. <b></b>.',
                        icon: "info",
                        timer: 150000,
                        allowOutsideClick: false,
                        timerProgressBar: true,
                        didOpen: () => {
                            Swal.showLoading()
                            const b = Swal.getHtmlContainer().querySelector('b')
                        }
                    }).then((result) => {
                        /* Read more about handling dismissals below */
                        if (result.dismiss === Swal.DismissReason.timer) {
                            window.location.href = "../index.php";
                        }
                    })
                    // Preparamos los datos para enviar por AJAX    
                var formData = {
                    email: email,
                    email2: email2,
                    cuil: sessionStorage.getItem('cuil'), // Obtener el CUIL de la sesión almacenada
                    id_usuario: sessionStorage.getItem('id_usuario') // Obtener el id_usuario de la sesión almacenada
                };
                // Realizamos la llamada AJAX
                $.ajax({
                    url: "../modelo/usuarios/crud/declaracionCorreo.php",
                    type: 'POST',
                    data: formData,
                    success: function(response) {
                        // var data = JSON.parse(response); 
                        if (response == 1) {
                            Swal.fire({
                                title: 'Éxito',
                                text: 'Correo electrónico registrado correctamente. Se enviara un CODIGO al mismo para que pueda validarlo.',
                                icon: 'success',
                                allowOutsideClick: false,
                                confirmButtonText: 'OK'
                            }).then(() => {
                                window.location.href = '../index.php'; // Redirigir al índice después del éxito
                            });
                        } else if (response == 0) {
                            Swal.fire({
                                title: 'Error',
                                text: 'Hubo un problema al registrar el correo electrónico. Vuelva a intentarlo.',
                                icon: 'error',
                                allowOutsideClick: false,
                                confirmButtonText: 'OK'
                            });
                        } else if (response == 2) {
                            Swal.fire({
                                title: 'Error',
                                text: 'Los correos no coinciden por favor vuelva a intentar.',
                                icon: 'error',
                                allowOutsideClick: false,
                                confirmButtonText: 'OK'
                            });
                        } else if (response == 6) {
                            Swal.fire({
                                title: 'Error',
                                text: 'El correo ya se encuentra ingresado.',
                                icon: 'error',
                                allowOutsideClick: false,
                                confirmButtonText: 'OK'
                            });
                        } else {
                            Swal.fire({
                                title: 'Error',
                                text: 'xxxxxxxxxxxxxxxxxxxxxxxxx' + response,
                                icon: 'error',
                                allowOutsideClick: false,
                                confirmButtonText: 'OK'
                            });
                        }


                    },
                    error: function(jqXHR, textStatus, errorThrown) {
                        Swal.fire({
                            title: 'Error',
                            text: 'Hubo un error en la solicitud: ' + errorThrown,
                            icon: 'error',
                            allowOutsideClick: false
                        });
                    }
                });
            }
        }); //cierre del cartel principal boton SI ¿Usted esta seguro de que los datos ingresados son correctos?
    return false;
}