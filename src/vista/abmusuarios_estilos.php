<?php
/* INCLUYO ENCABEZADO Y PIE DE PAGINA */

session_start();
//solo administrador del sistema
if(isset($_SESSION['cuil']) and ($_SESSION['rol'] == 2)){
include "../header.php";
include "../footer.php";

?>
<link rel="stylesheet" href="../public/css/abmusuarios.css">


<h1>Gestor de Usuarios</h1>
    <!-- Filtro por CUIL -->
<!--  <input type="text" id="filtroCuil" placeholder="Buscar por CUIL..." oninput="filtrarPorCuil()"> -->

    <button class="toggle-button">Ingresar nuevo usuario</button>
    <div class="form-container" id="formContainer">
        <h2>Formulario de Registro</h2>
        <!-- El formulario de registro envia los datos al js para luego procesarlo e insertarlo en la bd -->
        <form id="frmAgregarUsuario" method="POST" onsubmit="agregarNuevoUsuario()">
                <div class="form-group">
                    <label for="cuilNewUser">CUIL</label>
                    <input type="text" id="cuilNewUser" name="cuilNewUser" required>
                    <span id="cuilError" class="error-message"></span>
                </div>
                <div class="form-group">
                    <label for="nombreNewUser">Nombre</label>
                    <input type="text" id="nombreNewUser" name="nombreNewUser" required>
                    <span id="nombreError" class="error-message"></span>
                </div>
                <div class="form-group">
                    <label for="apellidoNewUser">Apellido</label>
                    <input type="text" id="apellidoNewUser" name="apellidoNewUser" required>
                    <span id="apellidoError" class="error-message"></span>
                </div>
                <div class="form-group">
                    <label for="legajoNewUser">Legajo</label>
                    <input type="text" id="legajoNewUser" name="legajoNewUser" required>
                    <span id="legajoError" class="error-message"></span>
                </div>
                <div class="form-group">
                    <label for="emailNewUser">Correo Electrónico</label>
                    <input type="email" id="emailNewUser" name="emailNewUser" placeholder="@hospitalposadas.gob.ar" required>
                </div>
                <div class="form-group">
                <!--   <label for="rol">Rol</label>
                    <select name="rol" id="rol" required>
                        <option value="" disabled selected>Elegir rol</option>
                        <option value="1">Empleado</option>
                        <option value="2">Administrador</option>
                    </select> -->
                </div>
                <br><br><br>
                <div class="form-group">
                    <button type="submit" id="botonRegistrar" class="btn btn-primary">Registrar</button>
                </div>
        </form>

    </div>
    


<!-- TABLA USUARIOS -->
<div>
    <input type="text" id="searchInput" placeholder="Buscar..." style="margin-bottom: 10px;">
    <select id="perPageSelect">
        <option value="5">5 por página</option>
        <option value="10" selected>10 por página</option>
        <option value="20">20 por página</option>
    </select>
</div>
<div class="table-container">
    <table id="tablaUsuariosDataTable">
        <thead>
            <tr>
                <th data-column="cuil" data-order="desc">Cuil</th>
                <th data-column="nombre" data-order="desc">Nombre</th>
                <th data-column="apellido" data-order="desc">Apellido</th>
                <th data-column="legajo" data-order="desc">Legajo</th>
                <th data-column="email" data-order="desc">Correo Electrónico</th>
                <th data-column="rol" data-order="desc">Rol</th>
                <th>Recibos</th>
                <th>Editar</th>
                <th>Deshabilitar</th>
            </tr>
        </thead>
        <tbody></tbody>
    </table>
</div>

<div  id="pagination">

</div>

<!-- FIN TABLA USUARIOS -->

<!-- Modal editar usuario -->
<div class="modal fade" id="modalEditarUsuarios" tabindex="-1" role="dialog" aria-labelledby="modalEditarUsuariosLabel" aria-hidden="true">
        <div class="modal-dialog" role="document">
             <div class="modal-content">
             <div class="modal-header">
            <h5 class="modal-title" id="modalEditarUsuariosLabel">Editar Usuario</h5>
             <button type="button" class="close" data-dismiss="modal" aria-label="Close">
            <span aria-hidden="true">&times;</span>
            </button>
    </div>
    <div class="modal-body">
        <!-- INICIO FORM -->
            <form id="formEditarUsuario">
                <div class="form-group">
                    <label for="cuilUpdate">CUIL</label>
                    <input type="text" class="form-control" id="cuilUpdate" name="cuilUpdate" readonly>
                </div>
                <div class="form-group">
                    <label for="nombreUpdate">Nombre</label>
                    <input type="text" class="form-control" id="nombreUpdate" name="nombreUpdate">
                </div>
                <div class="form-group">
                    <label for="apellidoUpdate">Apellido</label>
                    <input type="text" class="form-control" id="apellidoUpdate" name="apellidoUpdate">
                </div>
                <div class="form-group">
                    <label for="legajoUpdate">Legajo</label>
                    <input type="text" class="form-control" id="legajoUpdate" name="legajoUpdate">
                </div>
                <div class="form-group">
                    <label for="correoUpdate">Correo Electrónico</label>
                    <input type="email" class="form-control" id="correoUpdate" name="correoUpdate">
                </div>
                <div class="form-group">
                    <label for="rolUpdate">Rol</label>
                    <select class="form-control" id="rolUpdate" name="rolUpdate">
                    <option value="1">Rol 1</option>
                    <option value="2">Rol 2</option>
                    <!-- Agrega más roles según sea necesario -->
                    </select>
                </div>
                <button type="submit" class="btn btn-primary">Guardar Cambios</button>
            </form><!-- FIN FORM -->

    </div>
    </div>
</div>
</div>
    <!-- JavaScript para las acciones de los botones y el filtro -->
    <script> 

    // Cerrar el modal al hacer clic fuera de él
    window.onclick = function (event) {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    }

/* x */
</script>





<script>

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
        setupPagination();
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
            setupPagination();
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

            tr.innerHTML = `
                <td>${row.cuil}</td>
                <td>${row.nombre}</td>
                <td>${row.apellido}</td>
                <td>${row.legajo}</td>
                <td>${row.email}</td>
                <td>${row.rol}</td>
                <td><button class="btn btn-warning btn-sm" onclick="resetPassword('${row.id_usuario}')">Reestablecer contraseña</button></td>
                <td><button class="btn btn-warning btn-sm" data-toggle="modal" data-target="#modalEditarUsuarios" onclick='editarUsuarioVerInfo(${JSON.stringify(row)})'>Editar</button></td>
                <td><button class="btn btn-danger btn-sm" onclick="deshabilitarUsuario('${row.id_usuario}')">Deshabilitar</button></td>
            `;

            tableBody.appendChild(tr);
        });

        // Calcular y mostrar cantidad de páginas
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
            setupPagination();
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
        setupPagination();
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

/* function resetPassword(id) {
    console.log('Reestablecer contraseña para:', id);
} */

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
                $.ajax({
                    type: "POST",
                    url: "../modelo/usuarios/crud/resetPassword.php",
                    data: {
                        id_usuario: id_usuario
                    },
                    success: function(respuesta) {
                        respuesta = respuesta.trim();
                        if (respuesta == 1) {
                          /*   $('#tablaUsuariosDataTable').DataTable().ajax.reload();  *///REFRESCA EN TIEMPOR REAL LA TABLA
                            Swal.fire("Se envio una contraseña temporal al correo electrónico", "El usuario debera ingresarla y el sistema le pedira cambiarla.", "success");
                        } else {
                            Swal.fire("", "Error al reestablecer la contraseña de el usuario!" + respuesta, "error");
                        }
                    }
                });
            }
        });
}
function editarUsuarioVerInfo(data) {
    console.log('Editar usuario:', data);
}


function deshabilitarUsuario(id_usuario) {
    Swal.fire({
        title: "DESHABILITAR",
        text: "¿Desea Deshabilitar este usuario?",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: "SI",
        cancelButtonText: "NO",
        allowOutsideClick: false // Asegura que no se puede hacer clic fuera del modal
    }).then(resultado => {
        if (resultado.isConfirmed) {
            $.ajax({
                type: "POST",
                url: "../modelo/usuarios/crud/deshabilitarUsuario.php",
                data: { id_usuario: id_usuario },
                success: function(respuesta) {
                    respuesta = respuesta.trim();
                    if (respuesta == 1) {
                        Swal.fire("", "Se deshabilitó el usuario con éxito.", "success").then(() => {
                            // Aquí puedes realizar cualquier acción adicional después de deshabilitar
                            // Puedes recargar la tabla, actualizar la vista, etc.
                        });
                    } else {
                        Swal.fire("", "Error al deshabilitar el usuario! " + respuesta, "error");
                    }
                },
                error: function(xhr, textStatus, errorThrown) {
                    Swal.fire("", "Error al deshabilitar el usuario! " + errorThrown, "error");
                }
            });
        }
    });
}

</script>
<!-- <script src="https://cdn.datatables.net/2.0.7/js/dataTables.min.js"></script>  -->
<!-- <script src="../public/js/usuarios/usuarios.js"></script> -->


<?php
}
else 

{
    session_start();
    session_destroy();
    header("Location: ../index.php");
    exit();

}

?>