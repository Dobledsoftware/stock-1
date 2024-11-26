<?php

    class Conexion{
        public function conectar(){

            $servidor = "10.5.0.124";
            $usuario = "pablo";
            $password = "P4bl0";
            $db = "recibosdb";

            $conexion = mysqli_connect($servidor, $usuario, $password, $db);
            $conexion ->set_charset("utf8");
            return $conexion; 
          
        }

     
    }
   

    function formatearFecha($fecha){
        return date('g:i a', strtotime($fecha));
    }
    

    
