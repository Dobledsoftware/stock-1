import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import BarraLateral from "../components/BarraLateral";
import Stock from "./pantallas/Stock";
import Ventas from "./pantallas/Ventas";
import Administracion from "./pantallas/Administracion";
import '@fortawesome/fontawesome-free/css/all.min.css';


function App() {
  return (
    <Router>
      
      <div style={{ display: "flex" }}>
      
        <BarraLateral />
        
        <main style={{ marginLeft: "240px", padding: "20px", width: "100%" }}>
           {/* Agregamos el h1 con el cartel de bienvenida 
           <h1>Bienvenido a tu Panel de Administración</h1>*/}
          <Routes>
            <Route path="/stock" element={<Stock />} />
            <Route path="/ventas" element={<Ventas />} />
            <Route path="/administracion" element={<Administracion />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
