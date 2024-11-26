function restablecerContrasenia() {

    //cartel que pregunta si desea envuiar el correo electronico
    Swal.fire({

            title: "Validación y envio de correo electrónico.",
            text: "Se enviará un correo electrónico con los pasos a seguir para restablecer su contraseña, ¿Desea continuar?",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: "SI",
            cancelButtonText: "NO",
            allowOutsideClick: false
        })
        .then(resultado => {
            if (resultado.value) {
                //CARTEL DE CARGANDO
                Swal.fire({
                        title: 'Verificando, por favor no cierre el navegador.',
                        html: 'Aguarde, Su solicitud esta siendo procesada. <b></b>.',
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
                            window.location.href = "vistas/inicio.php";
                        }
                    }) //fin cartel cargando
                $.ajax({
                    type: "POST",
                    data: $('#fromRestablecerContrasenia').serialize(),
                    url: "procesos/usuarios/verificacion/verificacionRestablecerContrasenia.php",
                    success: function(respuesta) {
                        console.log(respuesta);
                        respuesta = respuesta.trim();
                        //***EMAIL NO COINCIDE con EMAIL2(1) */
                        if (respuesta == 1) {
                            const swalWithBootstrapButtons = Swal.mixin({
                                customClass: {
                                    confirmButton: 'btn btn-success',
                                },
                                buttonsStyling: false
                            })
                            swalWithBootstrapButtons.fire({
                                title: 'Los correo electrónico no coinciden.',
                                text: "Los campos de correo elecrónico deben ser iguales. vuelva a escribirlos.",
                                icon: 'error',
                                confirmButtonText: 'OK'
                            })
                        }
                        //** El email ingresado no coincide con un usuario registradd */
                        else if (respuesta == 4) {
                            const swalWithBootstrapButtons = Swal.mixin({
                                customClass: {
                                    confirmButton: 'btn btn-success',
                                },
                                buttonsStyling: false
                            })

                            swalWithBootstrapButtons.fire({
                                title: 'Correo electronico no registrado.',
                                text: "El correo electronico ingresado no se encuentra registrado en la base de datos, vuelva a intentarlo.",
                                icon: 'error',
                                confirmButtonText: 'OK'
                            })
                        }

                        //***retorna 3 si es correcto */
                        else if (respuesta == 3) {
                            const swalWithBootstrapButtons = Swal.mixin({
                                customClass: {
                                    confirmButton: 'btn btn-success',
                                },
                                buttonsStyling: false
                            })

                            swalWithBootstrapButtons.fire({
                                title: 'Correcto.',
                                text: "Se envio un enlace a su correo electronico para continuar el proceso de restablecimiento de su contraseña.",
                                icon: 'success',
                                confirmButtonText: 'OK'
                            }).then((result) => {
                                if (result.isConfirmed) {
                                    window.location = "index.html";

                                }
                            })

                        }



                        //***retorna 2 ya tiene un procesod e cambio de contraseña abierto no pueden haber 2 */
                        else if (respuesta == 2) {
                            const swalWithBootstrapButtons = Swal.mixin({
                                customClass: {
                                    confirmButton: 'btn btn-success',
                                },
                                buttonsStyling: false
                            })

                            swalWithBootstrapButtons.fire({
                                title: 'Usted ya tiene una solicitud de cambio de contraseña abierta.',
                                text: "Revise su casilla de entrada o seccion de SPAM de correo electronico..",
                                icon: 'error',
                                confirmButtonText: 'OK'
                            }).then((result) => {
                                if (result.isConfirmed) {
                                    window.location = "index.html";

                                }
                            })

                        } else if (respuesta == 5) {
                            const swalWithBootstrapButtons = Swal.mixin({
                                customClass: {
                                    confirmButton: 'btn btn-success',
                                },
                                buttonsStyling: false
                            })
                            swalWithBootstrapButtons.fire({
                                title: 'El correo electronico no se ha podido enviar.',
                                text: "por favor revise que el correo ingresado sea correcto.",
                                icon: 'error',
                                confirmButtonText: 'OK'
                            })
                        }
                        //***else FINAL ERROR DE SISTEMA */
                        else

                        {
                            swal.fire("error critico del sistema avisale al admin", respuesta, "advertence");

                        }



                    }

                });
                return false;
            } //ciere IF 
        }) //cierra pregunta si desea realizar el proceso
    return false;

}