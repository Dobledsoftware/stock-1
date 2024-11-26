function loginUsuario() {
    $.ajax({
        type: "POST",
        data: $('#formLogin').serialize(),
        url: "modelo/usuarios/crud/loginUsuario.php",
        success: function(respuesta) {
            respuesta = respuesta.trim();
            //declaracion de correo electronico 
            if (respuesta == 3) {
                let timerInterval
                Swal.fire({
                    title: 'Acceso concedido',
                    html: 'Bienvenido/a a la plataforma digital de Recibos de sueldos-HNAP. <b></b>.',
                    icon: "success",
                    timer: 2000,
                    timerProgressBar: true,
                    allowOutsideClick: false, // Asegura que no se puede hacer clic fuera del modal
                    didOpen: () => {
                        Swal.showLoading()
                        const b = Swal.getHtmlContainer().querySelector('b')
                    }
                }).then((result) => {
                    /* Read more about handling dismissals below */
                    if (result.dismiss === Swal.DismissReason.timer) {
                        Swal
                            .fire({
                                title: "Declaración de correo electrónico",
                                text: "No se ha encontrado un correo electrónico declarado en la base de datos. Por favor, ingrese uno. Este proceso se realiza solo una vez y puede requerir varios intentos de inicio de sesión para completarlo.",
                                icon: 'warning',
                                confirmButtonText: "OK",
                                allowOutsideClick: false // Asegura que no se puede hacer clic fuera del modal
                            })
                            .then(resultado => {
                                if (resultado.value) {
                                    window.location.href = "vista/declaracionCorreo.php";
                                }
                            });
                    }
                })
            }
            //validacion de correo electronico
            else if (respuesta == 2) {
                let timerInterval
                Swal.fire({
                    title: 'Acceso concedido',
                    html: 'Bienvenido/a a la plataforma digital de Recibos de sueldos-HNAP. <b></b>.',
                    icon: "success",
                    timer: 2000,
                    timerProgressBar: true,
                    didOpen: () => {
                        Swal.showLoading()
                        const b = Swal.getHtmlContainer().querySelector('b')
                    }
                }).then((result) => {
                    /* Read more about handling dismissals below */
                    if (result.dismiss === Swal.DismissReason.timer) {
                        Swal
                            .fire({
                                title: "Validación de correo electrónico pendiente",
                                text: "Usted debe validar su correo electrónico ingresando el codigo que se le envio al correo declarado. Este proceso se realiza solo una vez y puede requerir varios intentos de inicio de sesión para completarlo",
                                icon: 'warning',
                                confirmButtonText: "OK",
                                allowOutsideClick: false // Asegura que no se puede hacer clic fuera del modal
                            })
                            .then(resultado => {
                                if (resultado.value) {
                                    window.location.href = "vista/validacionCorreo.php";
                                }
                            });
                    }
                })
            } else if ((respuesta == 4) || (respuesta == 5)) {
                let timerInterval
                Swal.fire({
                    title: 'Acceso concedido',
                    html: 'Bienvenido/a a la plataforma digital de Recibos de sueldos-HNAP. <b></b>.',
                    icon: "success",
                    timer: 2000,
                    timerProgressBar: true,
                    didOpen: () => {
                        Swal.showLoading()
                        const b = Swal.getHtmlContainer().querySelector('b')
                    }
                }).then((result) => {
                    /* Read more about handling dismissals below */
                    if (result.dismiss === Swal.DismissReason.timer) {
                        Swal
                            .fire({
                                title: "Proceso de cambio de contraeña pendiente",
                                text: "A continuación usted debera ingresar una nueva contraseña.",
                                icon: 'warning',
                                confirmButtonText: "OK",
                                allowOutsideClick: false // Asegura que no se puede hacer clic fuera del modal
                            })
                            .then(resultado => {
                                if (resultado.value) {
                                    window.location.href = "vista/resetPassword.php";
                                }
                            });
                    }
                })
            } else if (respuesta == 1) {
                let timerInterval
                Swal.fire({
                    title: 'Acceso concedido',
                    html: 'Bienvenido/a a la plataforma digital de Recibos de sueldos-HNAP. <b></b>.',
                    icon: "success",
                    timer: 2000,
                    timerProgressBar: true,
                    didOpen: () => {
                        Swal.showLoading()
                        const b = Swal.getHtmlContainer().querySelector('b')
                    }
                }).then((result) => {
                    /* Read more about handling dismissals below */
                    if (result.dismiss === Swal.DismissReason.timer) {
                        window.location.href = "vista/tablaRecibos.php";
                    }
                })
            } else if (respuesta == 50) {
                Swal.fire("Acceso denegado.", "Usuario deshabilitado, porfavor comuniquese con un administrador.", "error");
            }
            /* else if (respuesta == 75) {
                        Swal.fire("Acceso denegado.", "Su usuario se encuentra pendiente a ser aprobado, sera notificado por correo electronico cuando este habilitado para usar el sistema.", "error");
                       } */
            else {
                Swal.fire("Acceso denegado.", "Usuario y contraseña incorrecta.", "error", respuesta);
            }
        }
    });
    return false;
}











document.addEventListener('DOMContentLoaded', function() {
    // Validación de campos del formulario
    var cuilInput = document.getElementById('cuil');
    if (cuilInput) {
        cuilInput.addEventListener('input', validateCuil);
        cuilInput.addEventListener('keydown', blockInvalidCuilCharacters);
    }

});

function validateCuil() {
    const cuilInput = document.getElementById('cuil');
    const submitBtn = document.getElementById('submitBtn');
    const cuilError = document.getElementById('cuil-error');

    // Eliminar cualquier carácter no numérico
    cuilInput.value = cuilInput.value.replace(/\D/g, '');

    // Verificar si el CUIL tiene exactamente 11 caracteres
    if (cuilInput.value.length === 11) {
        submitBtn.disabled = false;
        cuilError.style.display = 'none';
    } else {
        submitBtn.disabled = true;
        cuilError.style.display = 'block';
    }
}

function blockInvalidCuilCharacters(event) {
    if (!/\d/.test(event.key) && !['Backspace', 'Delete', 'ArrowLeft', 'ArrowRight', 'Tab'].includes(event.key)) {
        event.preventDefault();
    }
}
