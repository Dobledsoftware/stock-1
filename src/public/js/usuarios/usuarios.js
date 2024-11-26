/* FUNCION PRINCIPAL USUARIOS */
function agregarNuevoUsuario(event) {
    event.preventDefault(); // Evita la recarga de la página
    Swal
        .fire({
            title: "Ingreso de nuevo usuario al sistema.",
            text: "¿Usted esta seguro de que los datos ingresados son correctos?",
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
                    title: 'Registrando el nuevo usuario.',
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
                        //por ahora no va a hacer nada
                    }
                })

                const formData = $('#frmAgregarUsuario').serialize();
                $.ajax({
                    type: "POST",
                    data: formData,
                    url: "../modelo/usuarios/crud/agregarNuevoUsuario.php", // Cambiar a ruta absoluta
                    success: function(respuesta) {
                        respuesta = respuesta.trim();
                        if (respuesta == 1) {
                            Swal.fire("", "Agregado con éxito.", "success")
                                .then(() => {
                                    const formulario = document.getElementById("frmAgregarUsuario");
                                    formulario.reset();
                                    location.reload(); // Refrescar la página
                                });
                        } //
                        else if (respuesta == "incorrecto") {
                            document.getElementById('botonRegistrar').disabled = false;
                            Swal.fire("XD", "entro al crud " + respuesta, "error");
                        } else if (respuesta == "cuilError") {
                            document.getElementById('botonRegistrar').disabled = false;
                            Swal.fire("Error", "El cuil ya se encuentra ingresado: ", "error");
                        } else if (respuesta == "legajoError") {
                            document.getElementById('botonRegistrar').disabled = false;
                            Swal.fire("Error", "El legajo ya se encuentra ingresado: ", "error");
                        } else if (respuesta == "emailError") {
                            document.getElementById('botonRegistrar').disabled = false;
                            Swal.fire("Error", "El Correo electrónico ya se encuentra ingresado: ", "error");
                        } else {
                            Swal.fire("Error", "error de ejecucion: " + respuesta, "error");
                        }
                    }
                });
            }
        });
    return false;
}

/* Aqui se validan los campos para usuario nuevo FORMULARIO DE REGISTRO */
function agregarNuevoUsuarioValidaciones(event) {
    event.preventDefault(); // Evita el envío del formulario
    // Validar todos los campos antes de enviar el formulario
    validateCuil();
    validateNombre();
    validateApellido();
   /*  validateLegajo(); */

    // Obtener mensajes de error
    let cuilError = document.getElementById('cuilError').textContent;
    let nombreError = document.getElementById('nombreError').textContent;
    let apellidoError = document.getElementById('apellidoError').textContent;
   /*  let legajoError = document.getElementById('legajoError').textContent; */

    // Si no hay errores, enviar el formulario
    if (!cuilError && !nombreError && !apellidoError /* && !legajoError */) {
        event.target.submit();
    }
}
document.addEventListener('DOMContentLoaded', function() {
    // Validación de campos del formulario
    var cuilInput = document.getElementById('cuilNewUser');
    if (cuilInput) {
        cuilInput.addEventListener('input', validateCuil);
        cuilInput.addEventListener('keydown', blockInvalidCuilCharacters);
    }

    var nombreInput = document.getElementById('nombreNewUser');
    if (nombreInput) {
        nombreInput.addEventListener('input', validateNombre);
    }

    var apellidoInput = document.getElementById('apellidoNewUser');
    if (apellidoInput) {
        apellidoInput.addEventListener('input', validateApellido);
    }

   /*  var legajoInput = document.getElementById('legajoNewUser');
    if (legajoInput) {
        legajoInput.addEventListener('input', validateLegajo);
        legajoInput.addEventListener('keydown', blockInvalidLegajoCharacters);
    } */

    var emailInput = document.getElementById('emailNewUser');
    /*  if (emailInput) {
        emailInput.addEventListener('input', validateEmail);
     } */
});
//Validar CUIL
function validateCuil() {
    let cuilInput = document.getElementById('cuilNewUser');
    let cuil = cuilInput.value;
    let error = document.getElementById('cuilError');
    if (cuil === '') {
        error.textContent = '';
    } else if (!/^\d{9,11}$/.test(cuil) || parseInt(cuil, 11) <= 0) {
        error.textContent = 'El CUIL debe ser un número de 9 o 11 caracteres, no puede ser negativo ni cero.';
    } else {
        error.textContent = '';
    }
}

function blockInvalidCuilCharacters(event) {
    if (!/\d/.test(event.key) && !['Backspace', 'Delete', 'ArrowLeft', 'ArrowRight', 'Tab'].includes(event.key)) {
        event.preventDefault();
    }
}

//Validar nombre
function validateNombre() {
    let nombreInput = document.getElementById('nombreNewUser');
    let nombre = nombreInput.value;
    let error = document.getElementById('nombreError');
    if (nombre.trim() === '') {
        error.textContent = '';
    } else if (!/^[A-Za-záéíóúÁÉÍÓÚñÑ\s]+$/.test(nombre)) {
        error.textContent = 'El nombre debe contener solo letras y espacios.';
    } else {
        nombreInput.value = nombre.toUpperCase();
        error.textContent = '';
    }
}
//validar apellido
function validateApellido() {
    let apellidoInput = document.getElementById('apellidoNewUser');
    let apellido = apellidoInput.value;
    let error = document.getElementById('apellidoError');
    if (apellido.trim() === '') {
        error.textContent = '';
    } else if (!/^[A-Za-záéíóúÁÉÍÓÚñÑ\s]+$/.test(apellido)) {
        error.textContent = 'El apellido debe contener solo letras y espacios.';
    } else {
        apellidoInput.value = apellido.toUpperCase();
        error.textContent = '';
    }
}

/* function validateLegajo() {
    let legajoInput = document.getElementById('legajoNewUser');
    let legajo = legajoInput.value;
    let error = document.getElementById('legajoError');
    if (legajo === '') {
        error.textContent = '';
    } else if (!/^\d{5,6}$/.test(legajo) || parseInt(legajo, 6) < 0) {
        error.textContent = 'El Legajo debe ser un número de 5 u 6 caracteres y no puede ser negativo.';
    } else {
        error.textContent = '';
    }
} */

/* function blockInvalidLegajoCharacters(event) {
    if (!/\d/.test(event.key) && !['Backspace', 'Delete', 'ArrowLeft', 'ArrowRight', 'Tab'].includes(event.key)) {
        event.preventDefault();
    }
} */

document.addEventListener('DOMContentLoaded', function() {
    let dataUrl = '../modelo/usuarios/crud/cargaTablaUsuarios.php';
    let rowsPerPage = 10;
    let currentPage = 1;
    let data = [];
    let filteredData = [];

    const perPageSelect = document.getElementById('perPageSelect');
    const tableBody = document.querySelector('#tablaUsuariosDataTable tbody');
    const pagination = document.getElementById('pagination');

    perPageSelect.addEventListener('change', function() {
        rowsPerPage = parseInt(this.value);
        currentPage = 1;
        displayTable(currentPage);
        //setupPagination();
    });

    function fetchData() {
        fetch(dataUrl, {
                method: 'POST',
            })
            .then(response => response.json())
            .then(result => {
                data = result.data;
                filteredData = data;
                displayTable(currentPage);
                //setupPagination();
            })
            .catch(error => console.error('Error fetching data:', error));
    }

    function displayTable(page) {
        tableBody.innerHTML = '';

        const start = (page - 1) * rowsPerPage;
        const end = start + rowsPerPage;
        const pageData = filteredData.slice(start, end);

        pageData.forEach(row => {
            const tr = document.createElement('tr');
            /* se cambio row.cuil por row.id_usuario */
            tr.innerHTML = `
                <td>${row.cuil}</td>
                <td>${row.nombre}</td>
                <td>${row.apellido}</td>
                <td>${row.legajo}</td>
                <td>${row.email}</td>
                <td><button class="btn btn-warning btn-sm" onclick="resetPassword('${row.id_usuario}')">Reestablecer contraseña</button></td> 
                <td><button class="btn btn-warning btn-sm" data-toggle="modal" data-target="#modalEditarUsuarios" onclick='editarUsuarioVerInfo(${JSON.stringify(row)})'>Editar</button></td>
            `;
            tableBody.appendChild(tr);
        });


        const totalPages = Math.ceil(filteredData.length / rowsPerPage);
        pagination.innerHTML = '';
        const prevButton = createPaginationButton('Anterior', currentPage > 1 ? currentPage - 1 : 1);
        pagination.appendChild(prevButton);

        let startPage = currentPage - 2;
        if (startPage < 1) {
            startPage = 1;
        }
        let endPage = startPage + 4;
        if (endPage > totalPages) {
            endPage = totalPages;
            startPage = endPage - 4;
            if (startPage < 1) {
                startPage = 1;
            }
        }

        for (let i = startPage; i <= endPage; i++) {
            const button = createPaginationButton(i, i);
            pagination.appendChild(button);
        }

        const nextButton = createPaginationButton('Siguiente', currentPage < totalPages ? currentPage + 1 : totalPages);
        pagination.appendChild(nextButton);
    }

    function createPaginationButton(text, page) {
        const button = document.createElement('button');
        button.innerText = text;
        button.classList.add('btn', 'btn-sm');
        button.addEventListener('click', () => {
            currentPage = page;
            displayTable(currentPage);
            //setupPagination();
        });
        return button;
    }

    function filterData(searchTerm) {
        filteredData = data.filter(row => {
            return Object.values(row).some(value =>
                String(value).toLowerCase().includes(searchTerm.toLowerCase())
            );
        });
        currentPage = 1;
        displayTable(currentPage);
        //setupPagination();
    }

    function sortData(column, order) {
        filteredData.sort((a, b) => {
            if (a[column] < b[column]) return order === 'asc' ? -1 : 1;
            if (a[column] > b[column]) return order === 'asc' ? 1 : -1;
            return 0;
        });
        displayTable(currentPage);
    }

    document.getElementById('searchInput').addEventListener('input', function() {
        filterData(this.value);
    });

    document.querySelectorAll('#tablaUsuariosDataTable th[data-column]').forEach(th => {
        th.addEventListener('click', function() {
            const column = this.getAttribute('data-column');
            const order = this.getAttribute('data-order');
            sortData(column, order);
            this.setAttribute('data-order', order === 'asc' ? 'desc' : 'asc');
        });
    });

    fetchData();


});



//editar usuario 
function editarUsuarioVerInfo(usuario) {
    /*  $('#modalEditarUsuarios').modal('show'); */
    document.getElementById('id_usuarioUpdate').value = usuario.id_usuario;
    document.getElementById('cuilUpdate').value = usuario.cuil;
    document.getElementById('nombreUpdate').value = usuario.nombre;
    document.getElementById('apellidoUpdate').value = usuario.apellido;
    document.getElementById('legajoUpdate').value = usuario.legajo;
    document.getElementById('correoUpdate').value = usuario.email;
    document.getElementById('rolUpdate').value = usuario.rol;
}




function editarUsuario() {
    Swal.fire({
        title: "Actualizar datos",
        text: "¡Está seguro de actualizar los datos del usuario?",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: "SI",
        cancelButtonText: "NO",
        allowOutsideClick: false
    }).then(resultado => {
        if (resultado.value) {
            var id_usuarioUpdate = $('#id_usuarioUpdate').val();
            var cuilUpdate = $('#cuilUpdate').val();
            var nombreUpdate = $('#nombreUpdate').val();
            var apellidoUpdate = $('#apellidoUpdate').val();
            var legajoUpdate = $('#legajoUpdate').val();
            var correoUpdate = $('#correoUpdate').val();
            var rolUpdate = $('#rolUpdate').val();

            $.ajax({
                type: "POST",
                url: "../modelo/usuarios/crud/editarUsuario.php",
                data: {
                    id_usuarioUpdate: id_usuarioUpdate,
                    cuilUpdate: cuilUpdate,
                    nombreUpdate: nombreUpdate,
                    apellidoUpdate: apellidoUpdate,
                    legajoUpdate: legajoUpdate,
                    correoUpdate: correoUpdate,
                    rolUpdate: rolUpdate
                },
                success: function(respuesta) {
                    if (respuesta == 1) {
                        //$('#modalEditarUsuarios').modal('hide'); // Cerrar el modal
                        Swal.fire("¡Éxito en la actualización!.", "Los datos se actualizaron con éxito.", "success")
                            .then(() => {
                                location.reload(); // Refrescar la página
                            });
                        //verifica que el cuil existe
                    } else if (respuesta == 3) {
                        Swal.fire("Error", "El CUIL ya existe, verifique que la información sea correcta.", "error");
                    }
                    //verifica que el legajo existe
                    else if (respuesta == 4) {
                        Swal.fire("Error", "El LEGAJO ya existe, verifique que la información sea correcta.", "error");
                    }
                    //verifica que el correo
                    else if (respuesta == 5) {
                        Swal.fire("Error", "El Correo electrónico ya existe, verifique que la información sea correcta.", "error");
                    }
                    //verifica que los datos no se hayan modificado con respecto a que no se toco nada en el formulario
                    else if (respuesta == 2) {
                        Swal.fire("Error", "No se detecto que usted haya modificado algún datos, verifique nuevamente.", "error");
                    } else {
                        Swal.fire("Error", "xxxxx" + respuesta, "error");
                    }
                },
                error: function(xhr, status, error) {
                    console.error("Error en la solicitud AJAX:", status, error);
                    Swal.fire("", "Error en la solicitud AJAX: " + error, "error");
                }
            });
        }
    });

    return false;
}




/* Funcion deshabilitar Usuario */
function deshabilitarUsuario(id_usuario) {
    Swal
        .fire({
            title: "DESHABILITAR",
            text: "Desea Deshabilitar este usuario?",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: "SI",
            cancelButtonText: "NO",
            allowOutsideClick: false // Asegura que no se puede hacer clic fuera del modal
        })
        .then(resultado => {
            if (resultado.value) {
                $.ajax({
                    type: "POST",
                    url: "../modelo/usuarios/crud/deshabilitarUsuario.php",
                    data: {
                        id_usuario: id_usuario
                    },
                    success: function(respuesta) {
                        respuesta = respuesta.trim();
                        if (respuesta == 1) {
                            $('#tablaUsuariosDataTable').DataTable().ajax.reload(); //REFRESCA EN TIEMPOR REAL LA TABLA
                            Swal.fire("", "Se deshabilito el usuario con éxito.", "success");
                        } else {
                            Swal.fire("", "Error al deshabilitar el usuario!" + respuesta, "error");
                        }
                    }
                });
            }
        });
}


/* Funcion para ver mis datos */
function misDatos(id_usuario) {
    $.ajax({
        type: "POST",
        data: { id_usuario: id_usuario },
        url: "../modelo/usuarios/crud/misDatos.php",
        success: function(respuesta) {
            respuesta = jQuery.parseJSON(respuesta);
            if (!respuesta.error) {
                $('#userId').text(respuesta['id_usuarioMisDatos']);
                $('#userCuil').text(respuesta['cuilMisDatos']);
                $('#userApellidoYNombreConcatenado').text(respuesta['nombreMisDatos'] + ' ' + respuesta['apellidoMisDatos']);
                $('#userName').text(respuesta['nombreMisDatos']);
                $('#userLastName').text(respuesta['apellidoMisDatos']);
                $('#userLegajo').text(respuesta['legajoMisDatos']);
                $('#userEmail').text(respuesta['emailMisDatos']);
            } else {
                alert(respuesta.error);
            }
        }
    });
}



function resetPassword(id_usuario) {
    Swal
        .fire({
            title: "Reestablecer contraseña",
            text: "¿Desea reestablecer la contraseñar de este usuario?",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: "SI",
            cancelButtonText: "NO",
            allowOutsideClick: false // Asegura que no se puede hacer clic fuera del modal
        }).then(resultado => {
            if (resultado.value) {
                document.getElementById('botonRegistrar').disabled = true;
                //CARTEL DE CARGANDO
                Swal.fire({
                    title: 'Reestableciendo la contraseña del usuario.',
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
                        //por ahora no va a hacer nada
                    }
                })
                $.ajax({
                    type: "POST",
                    url: "../modelo/usuarios/crud/resetPassword.php",
                    data: {
                        id_usuario: id_usuario
                    },
                    success: function(respuesta) {
                        respuesta = respuesta.trim();
                        if (respuesta == 1) {
                            Swal.fire({
                                title: 'Éxito',
                                text: 'Se envio una contraseña temporal al correo electrónico. El usuario debera ingresarla y el sistema le pedira cambiarla.',
                                icon: 'success',
                                allowOutsideClick: false,
                                confirmButtonText: 'OK'
                            }).then(() => {
                                location.reload(); // Redirigir al índice después del éxito
                            });
                        } else if (respuesta == 0) {
                            //$('#tablaUsuariosDataTable').DataTable().ajax.reload(); //REFRESCA EN TIEMPOR REAL LA TABLA
                            Swal.fire("Error", "El usuario tiene un proceso de cambio de contraseña en proceso", "error");

                        } else if (respuesta == 2) {
                            //$('#tablaUsuariosDataTable').DataTable().ajax.reload(); //REFRESCA EN TIEMPOR REAL LA TABLA
                            Swal.fire("Error", "El usuario no tiene correo electrónico VALIDADO ", "error");
                        } else if (respuesta == 3) {
                            //$('#tablaUsuariosDataTable').DataTable().ajax.reload(); //REFRESCA EN TIEMPOR REAL LA TABLA
                            Swal.fire("Error", "El usuario no tiene correo electrónico, debe asignale uno y posteriormente reestablecer la contraseña.", "error");
                        } else {
                            Swal.fire("", "Error al reestablecer la contraseña de el usuario!" + respuesta, "error");

                        }
                    }


                });
            }
        });
}
