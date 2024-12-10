import React, { useState, useEffect, useRef } from "react";

const LectorCodigoBarras = ({ onBuscar }) => {
  const [codigo, setCodigo] = useState("");
  const inputRef = useRef(null);

  useEffect(() => {
    // Enfocar automáticamente en el campo de entrada al cargar la página
    if (inputRef.current) {
      inputRef.current.focus();
    }
  }, []);

  const manejarCambio = (e) => {
    setCodigo(e.target.value);
  };

  const manejarKeyPress = (e) => {
    // Detectar si se presionó Enter
    if (e.key === "Enter" && codigo.trim() !== "") {
      onBuscar(codigo.trim()); // Ejecutar la búsqueda
      setCodigo(""); // Limpiar el campo después de la búsqueda
    }
  };

  return (
    <div style={{ display: "none" }}>
      {/* Campo oculto para capturar el código de barras */}
      <input
        type="text"
        value={codigo}
        onChange={manejarCambio}
        onKeyPress={manejarKeyPress}
        ref={inputRef}
      />
    </div>
  );
};

export default LectorCodigoBarras;
