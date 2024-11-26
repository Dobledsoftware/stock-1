<?php
/* INCLUYO ENCABEZADO Y PIE DE PAGINA */

session_start();
//solo administrador del sistema
if(isset($_SESSION['cuil']) and ($_SESSION['rol'] == 2)){
include "../header.php";
include "../footer.php";

?>
<link rel="stylesheet" href="../public/css/abmusuarios.css">
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
<script src="https://cdn.datatables.net/2.0.7/js/dataTables.min.js"></script> 
<script src="../public/js/usuarios/usuarios.js"></script>
<h1>Gestor de Usuarios</h1>
    <!-- Filtro por CUIL -->
<!--  <input type="text" id="filtroCuil" placeholder="Buscar por CUIL..." oninput="filtrarPorCuil()"> -->
    <button class="toggle-button" data-toggle="modal" data-target="#modalAgregarUsuarios">Ingresar nuevo usuario</button>
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
                <th>Contraseña</th>
                <th>Editar</th>
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
            <div class="modal-header"><!-- inicio modal header -->
                <h5 class="modal-title" id="modalEditarUsuariosLabel">Editar Usuario</h5>
                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                <span aria-hidden="true">&times;</span>
                </button>
            </div><!-- fin modal header -->
                <div class="modal-body">
                    <!-- INICIO FORM -->
                        <form id="formEditarUsuario" method="POST" onsubmit=" return editarUsuario()">
                        <div class="form-group">
                                <input type="text" class="form-control" id="id_usuarioUpdate" name="id_usuarioUpdate" readonly hidden>
                            </div>
                            <div class="form-group">
                                <label for="cuilUpdate">CUIL</label>
                                <input type="text" class="form-control" id="cuilUpdate" name="cuilUpdate" >
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

                </div><!-- fin fiv class -->
        </div>
    </div>
</div><!-- fin modal  -->
<!-- Modal editar Agregar usuario -->
<div class="modal fade" id="modalAgregarUsuarios" tabindex="-1" role="dialog" aria-labelledby="modalAgregarUsuarios" aria-hidden="true">
    <div class="modal-dialog" role="document">
        <div class="modal-content">
            <div class="modal-header"><!-- inicio modal header -->
                <h5 class="modal-title" id="modalAgregarUsuarios">Agregar nuevo Usuario</h5>
                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                <span aria-hidden="true">&times;</span>
                </button>
            </div><!-- fin modal header -->
                <div class="modal-body">
                    <!-- INICIO FORM -->
                            <form id="frmAgregarUsuario" method="POST" onsubmit="agregarNuevoUsuario(event)">
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
                                    <input type="text" id="legajoNewUser" name="legajoNewUser" >
                                    <span id="legajoError" class="error-message"></span>
                                </div>
                                <div class="form-group">
                                    <label for="emailNewUser">Correo Electrónico</label>
                                    <input type="email" id="emailNewUser" name="emailNewUser" placeholder="@hospitalposadas.gob.ar" required>
                                </div>
                                    <!-- <div class="form-group">
                                    <label for="rol">Rol</label>
                                        <select name="rol" id="rol" required>
                                            <option value="" disabled selected>Elegir rol</option>
                                            <option value="1">Empleado</option>
                                            <option value="2">Administrador</option>
                                        </select> 
                                    </div> -->
                        <br><br><br>
                        <div class="form-group">
                            <button type="submit" id="botonRegistrar" class="btn btn-primary">Registrar</button>
                        </div>
                </form>


                </div><!-- fin fiv class -->
        </div>
    </div>
</div><!-- fin modal  -->
<script>
    document.addEventListener("DOMContentLoaded", function() {
    // Definir la función aquí
    function verResultados(idUsuario) {
        const url = `tablaRecibosUsuarios.php?id_usuario=${idUsuario}`;
        window.open(url, '_blank');
    }
});

</script>

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
