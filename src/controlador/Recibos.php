

<?php
    include "Conexion.php";
    //include "mailRegistro2.php";    
   // include "mailRestablecerContrasenia.php";   
    use PHPMailer\PHPMailer\PHPMailer;
    use PHPMailer\PHPMailer\Exception;
    //require 'PHPMailer/src/Exception.php';
    //require 'PHPMailer/src/PHPMailer.php';
    //require 'PHPMailer/src/SMTP.php'; 
                                /* require '../vendor/autoload.php'; */
class Recibos extends Conexion{
    public function cargaTablaRecibos($id_usuario, $periodo, $cuil) {
        // Crear una instancia de la clase Conexion
        $conexion = new Conexion();
        // Obtener la conexión utilizando el método conectar()
        $conn = $conexion->conectar();
    
        // Consulta SQL para buscar recibos por id_usuario o cuil
        $sql = "SELECT recibos.descripcion_archivo, recibos_periodos.periodo, recibos.id_recibo 
                FROM recibos_periodos
                JOIN recibos ON recibos.id_periodo = recibos_periodos.id_periodo 
                WHERE recibos_periodos.estado = 'Activado'
                AND recibos_periodos.periodo = '$periodo' 
                AND (recibos.id_usuario = '$id_usuario' OR recibos.cuil = '$cuil')
                AND recibos.estado='Activado'
                ORDER BY recibos.fecha_correspondencia ASC";
        
        // Ejecutar consulta
        $query = $conn->query($sql);
        
        // Preparar datos para la respuesta
        $data = array();
        while ($row = $query->fetch_assoc()) {
            $data[] = $row;
        }
        
        // Crear respuesta en formato JSON
        $response = array(
            "draw" => intval($_POST['draw']), // Número de petición (es igual al número de peticiones hechas)
            "recordsTotal" => count($data), // Total de registros sin ningún filtro
            "recordsFiltered" => count($data), // Total de registros con el filtro aplicado (en este caso, no hay filtro)
            "data" => $data // Datos a mostrar en la tabla
        );
        
        // Enviar respuesta
        echo json_encode($response);
    }
    



            public function cargarPeriodos($id_usuario, $cuil) {                
                $conexion = new Conexion();
                $conn = $conexion->conectar();   
            
                // Buscar recibos por id_usuario o por cuil
                $sql = "SELECT rp.periodo 
                        FROM recibos r
                        JOIN recibos_periodos rp ON r.id_periodo = rp.id_periodo
                        WHERE r.id_usuario = '$id_usuario' OR r.cuil = '$cuil'
                        GROUP BY rp.periodo 
                        ORDER BY STR_TO_DATE(CONCAT(SUBSTRING(rp.periodo, 1, 2), '-01-', SUBSTRING(rp.periodo, 3, 4)), '%m-%d-%Y') ASC;";
                
                $query = $conn->query($sql);
                // Procesar los resultados
                $data = array();
                while ($row = $query->fetch_assoc()) {
                    $data[] = $row['periodo'];
                } 
            
                echo json_encode($data); 
            }   
           /*  public function cargaTablaRecibosDesdeAdmDelSistema() {
                // Crear una instancia de la clase Conexion
                $conexion = new Conexion();
                // Obtener la conexión utilizando el método conectar()
                $conn = $conexion->conectar();    
            
                $sql = "SELECT id_archivo, archivo, fecha_correspondencia, fecha_subida, email, rol FROM usuarios WHERE habilitado = '1'";    
            
                // Ejecutar consulta
                $query = $conn->query($sql);    
            
                // Preparar datos para la respuesta
                $data = array();
                while ($row = $query->fetch_assoc()) {
                    $data[] = $row;
                }   
            
                // Crear respuesta en formato JSON
                $response = array(
                    "draw" => intval($_POST['draw']), // Número de petición (es igual al número de peticiones hechas)
                    "recordsTotal" => count($data), // Total de registros sin ningún filtro
                    "recordsFiltered" => count($data), // Total de registros con el filtro aplicado (en este caso, no hay filtro)
                    "data" => $data // Datos a mostrar en la tabla
                );
                // Enviar respuesta
                echo json_encode($response);   
            } */


        public function verRecibos($id_recibo)
            {   // Crear una instancia de la clase Conexion
                $conexion = new Conexion();
                // Obtener la conexión utilizando el método conectar()
                $conn = $conexion->conectar();
                $sql = "SELECT archivo FROM recibos 
                join recibos_periodos on recibos.id_periodo = recibos_periodos.id_periodo
                WHERE recibos.id_recibo = '$id_recibo' and recibos_periodos.estado = 'Activado'";
                // Ejecutar consulta
                $query = $conn->query($sql);
                // Preparar datos para la respuesta
                $data = array();
                while ($row = $query->fetch_assoc()) {
                    $data[] = $row;
                }
                // Crear respuesta en formato JSON
                $response = array(
                    //"draw" => intval($_POST['draw']), // Número de petición (es igual al número de peticiones hechas)
                    "recordsTotal" => count($data), // Total de registros sin ningún filtro
                    "recordsFiltered" => count($data), // Total de registros con el filtro aplicado (en este caso, no hay filtro)
                    "data" => $data // Datos a mostrar en la tabla
                );
                // Registrar en la base de datos logs
              /*   $sql = "INSERT INTO `recibos_logs`(`id_usuario`, `id_recibo`) 
                VALUES ('$id_usuario', '$id_recibo')";
                $conn->query($sql); */
                echo json_encode($response);     
            }
                }//fin clase
                