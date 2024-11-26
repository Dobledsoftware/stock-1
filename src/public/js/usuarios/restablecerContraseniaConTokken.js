function restablecerContraseniaConTokken() {

    $.ajax({
        type: "POST",
        data: $('#formRestablecerContraseniaConTokken').serialize(),
        url: "procesos/usuarios/verificacion/verificacionRestablecerContraseniaConTokken.php",
        success: function(respuesta) {
            console.log(respuesta);
            respuesta = respuesta.trim();
            //***password no coincide con password2(1) */
            if (respuesta == 1) {
                const swalWithBootstrapButtons = Swal.mixin({
                    customClass: {
                        confirmButton: 'btn btn-success',
                    },
                    buttonsStyling: false
                })

                swalWithBootstrapButtons.fire({
                    title: 'Las contraseñas no coinciden.',
                    text: "Los campos de contraseña deben ser iguales. vuelva a escribirlos.",
                    icon: 'error',
                    confirmButtonText: 'OK'
                })
            }
            //** El email que se envio por url fue modificado en el proceso de validacion no coincide */
            else if (respuesta == 4) {
                const swalWithBootstrapButtons = Swal.mixin({
                    customClass: {
                        confirmButton: 'btn btn-success',
                    },
                    buttonsStyling: false
                })

                swalWithBootstrapButtons.fire({
                    title: 'Error de enlace.',
                    text: "Porfavor ingrese por el enlace que le enviamos a su correo electronico.",
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
                    text: "La contraseña fue cambiada con éxito, pruebe ingresando al sistema.",
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
                    title: 'Error de enlace.',
                    text: "Porfavor ingrese por el enlace que le enviamos a su correo electronico.",
                    icon: 'error',
                    confirmButtonText: 'OK'
                }).then((result) => {
                    if (result.isConfirmed) {
                        window.location = "index.html";

                    }
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

}