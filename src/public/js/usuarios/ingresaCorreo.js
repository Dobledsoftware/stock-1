function ingresaCorreo() {
    Swal
        .fire({
            title: "Registro de usuario.",
            text: "¿Usted esta seguro que los datos ingresados son correctos?",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: "SI",
            cancelButtonText: "NO",
            allowOutsideClick: false
        })
        .then(resultado => {
            if (resultado.value) {
                document.getElementById('botonRegistrar').disabled = true;
                //CARTEL DE CARGANDO
                Swal.fire({
                    title: 'Registrando el Correo.',
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
                        window.location.href = "vistas/inicio.php";
                    }
                })
                $.ajax({
                    type: "POST",
                    data: $('#formVerificarCorreo').serialize(),
                    url: "modelo/usuarios/verificacion/verificacionCorreo.php",
                    success: function(respuesta) {
                        document.getElementById('botonRegistrar').disabled = false;
                        console.log(respuesta);
                        respuesta = respuesta.trim();
                        //***si vuelve (0) es por que El email ingresado ya se encuentra en uso
                        if (respuesta == 0) {
                            botonRegistrar.disabled = false;
                            const swalWithBootstrapButtons = Swal.mixin({
                                customClass: {
                                    confirmButton: 'btn btn-success',
                                },
                                buttonsStyling: false
                            })
                            swalWithBootstrapButtons.fire({
                                allowOutsideClick: false,
                                title: 'Este email ya se encuentra ingresado en la base de datos.',
                                text: "por favor ingrese un email diferente o contáctese con el administrador.",
                                icon: 'error',
                                confirmButtonText: 'OK'
                            })
                        }


                        //***si vuelve 4 es por que El dni ingresado ya se encuentra en uso
                        else if (respuesta == 4) {
                            const swalWithBootstrapButtons = Swal.mixin({
                                customClass: {
                                    confirmButton: 'btn btn-success',
                                    icon: 'error',
                                },
                                buttonsStyling: false
                            })
                            swalWithBootstrapButtons.fire({
                                allowOutsideClick: false,
                                title: 'El Cuil ya se encuentra ingresado en la base de datos.',
                                text: "por favor ingrese otro Cuil.",
                                icon: 'error',
                                confirmButtonText: 'OK'
                            })
                        }
                        //***si vuelve (3) es por que la carga se hizo exitosamente 
                        else if (respuesta == 3) {
                            const swalWithBootstrapButtons = Swal.mixin({
                                customClass: {
                                    confirmButton: 'btn btn-success',
                                },
                                buttonsStyling: false
                            })
                            swalWithBootstrapButtons.fire({
                                allowOutsideClick: false,
                                title: 'Los datos se cargarón correctamente',
                                text: "Se envió un correo eléctronico con un código de verificación, revise su bandeja de entrada y/o su bandeja de SPAM.",
                                icon: 'success',
                                confirmButtonText: 'OK'
                            }).then((result) => {
                                if (result.isConfirmed) {
                                    window.location = "index.html";
                                }
                            })
                        }
                        if (respuesta != 5) {
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
                    }
                });
            }
        });
    return false;

}