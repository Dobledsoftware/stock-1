<?php
include "../controlador/Conexion.php";
// Suponiendo que $mysqli es tu conexión a la base de datos y $id_usuario es el ID del usuario actual
// Crear una instancia de la clase Conexion
$conexion = new Conexion();
// Obtener la conexión utilizando el método conectar()
$conn = $conexion->conectar();   

$query = $mysqli->query("SELECT rp.periodo FROM recibos r
                         JOIN recibos_periodos rp ON r.id_periodo = rp.id_periodo
                         WHERE r.id_usuario = $id_usuario");

if ($query) {
    $periodos = array();
    while ($valores = mysqli_fetch_array($query)) {
        $periodos[] = $valores['periodo'];
    }
    echo json_encode($periodos);
} else {
    echo json_encode(array('error' => 'Error al cargar los periodos'));
}
?>
