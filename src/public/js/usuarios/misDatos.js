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