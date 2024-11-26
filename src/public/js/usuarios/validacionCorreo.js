
function validacionCorreo() {
    // Obtenemos los valores de los inputs de correo electrónico
    var codigo = document.getElementById('codigo').value;
    Swal.fire({
        title: "Validación de correo electrónico.",
        text: "¿Usted está seguro de que los datos ingresados son correctos?",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: "SI",
        cancelButtonText: "NO",
        allowOutsideClick: false
    }).then((resultado) => {
        if (resultado.isConfirmed) {
            document.getElementById('Validar').disabled = true;
            //CARTEL DE CARGANDO
            Swal.fire({
                title: 'Validando.',
                html: 'Por favor aguarde, se esta procesando su solicitud. <b></b>',
                icon: "info",
                timer: 150000,
                allowOutsideClick: false,
                timerProgressBar: true,
                didOpen: () => {
                    Swal.showLoading()
                    const b = Swal.getHtmlContainer().querySelector('b')
                }
            });
            // Preparamos los datos para enviar por AJAX    
            var formData = {
                codigo: codigo,
                cuil: sessionStorage.getItem('cuil'), // Obtener el CUIL de la sesión almacenada
                id_usuario: sessionStorage.getItem('id_usuario') // Obtener el id_usuario de la sesión almacenada
            };
            // Realizamos la llamada AJAX
            $.ajax({
                url: "../modelo/usuarios/crud/validacionCorreo.php",
                type: 'POST',
                data: formData,
                success: function(response) {
                    if (response == 1) {
                        Swal.fire({
                            title: 'Éxito',
                            text: 'Correo electrónico validado correctamente. Vuelva a iniciar la sesión.',
                            icon: 'success',
                            allowOutsideClick: false,
                            confirmButtonText: 'OK'
                        }).then(() => {
                            window.location.href = '../index.php'; // Redirigir al índice después del éxito
                        });
                    } else if (response == 0) {
                        Swal.fire({
                            title: 'Error',
                            text: 'Código incorrecto. Vuelva a intentarlo.',
                            icon: 'error',
                            allowOutsideClick: false,
                            confirmButtonText: 'OK'
                        }).then((result) => {
                            if (result.isConfirmed) {
                                document.getElementById('codigo').value = ''; // Eliminar el contenido de la caja de texto
                                location.reload(); // Refrescar la página
                            }
                        });
                    } else {
                        Swal.fire({
                            title: 'Error',
                            text: 'Caputre la pantalla y comuniquese con un administrador' + response,
                            icon: 'error',
                            allowOutsideClick: false,
                            confirmButtonText: 'OK'
                        }).then((result) => {
                            if (result.isConfirmed) {
                                document.getElementById('codigo').value = ''; // Eliminar el contenido de la caja de texto
                                location.reload(); // Refrescar la página
                            }
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
    });
    return false; //ojo, sin el return FALSE el cartel queda en el limbo ponerlo siempre.
}





/* 




function ValidacionCorreo() {

    $.ajax({
        type: "POST",
        data: $('#formVerificarCodigo').serialize(),
        url: "procesos/usuarios/verificacion/verificacionCodigo.php",
        success: function(respuesta) {
            respuesta = respuesta.trim();
            //CODIGO DE VERIFICACION INCORRECTO (1) 
            if (respuesta == 1) {
                const swalWithBootstrapButtons = Swal.mixin({
                    customClass: {
                        confirmButton: 'btn btn-success',
                    },
                    buttonsStyling: false
                })
                swalWithBootstrapButtons.fire({
                    title: 'Código de verificacion Incorrecto.',
                    text: "Revise el código de seguridad enviado a su correo electrónico.",
                    icon: 'error',
                    confirmButtonText: 'OK'
                })
            }
            //se terminaron los intentos (2) 
            else if (respuesta == 2) {
                const swalWithBootstrapButtons = Swal.mixin({
                    customClass: {
                        confirmButton: 'btn btn-success',
                    },
                    buttonsStyling: false
                })

                swalWithBootstrapButtons.fire({
                    title: 'Se terminaron sus 3 intentos de ingresar con el código de seguridad',
                    text: "Su usuario se encuentra BLOQUEADO para usar el sistema. Comuniquese con un administrador",
                    icon: 'error',
                    confirmButtonText: 'OK'
                }).then((result) => {
                    if (result.isConfirmed) {
                        window.location = "index.html";
                    }
                })
            }
            //retorna 3 si es correcto 
            else if (respuesta == 3) {
                const swalWithBootstrapButtons = Swal.mixin({
                    customClass: {
                        confirmButton: 'btn btn-success',
                    },
                    buttonsStyling: false
                })
                swalWithBootstrapButtons.fire({
                    title: 'Código de verificación correcto. Correo electronico validado',
                    text: "Usted ahora puede hacer uso del sistema comdis-HNAP.",
                    icon: 'success',
                    confirmButtonText: 'OK'
                }).then((result) => {
                    if (result.isConfirmed) {
                        window.location = "index.html";
                    }
                })
            }
            //else FINAL ERROR DE SISTEMA 
            else {
                swal.fire("Error de carga", respuesta, "advertence");
            }
        }
    });
    return false;

} */