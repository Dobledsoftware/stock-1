import React, { useState, useEffect } from "react";
import Categorias from "../components/Categorias";
import Marcas from "../components/Marcas";
import Proveedores from "../components/Proveedores";
import Almacenes from "../components/Almacen";
import TablaProductos from "../components/TablaProductos";
import AgregarProducto from "../components/AgregarProducto";
import "../styles/configuracion.css";

const Config = () => {
  const [tabSeleccionada, setTabSeleccionada] = useState("TablaProductos");
  const [modalProductoVisible, setModalProductoVisible] = useState(false);
  const [productos, setProductos] = useState([]);
  const [marcas, setMarcas] = useState([]);
  const [categorias, setCategorias] = useState([]);
  const [proveedores, setProveedores] = useState([]);
  const [almacenes, setAlmacenes] = useState([]);

  // Abrir y cerrar el modal de productos
  const manejarAbrirModalProducto = () => setModalProductoVisible(true);
  const manejarCerrarModalProducto = () => setModalProductoVisible(false);

  // Cuando se agrega un producto nuevo
  const manejarProductoAgregado = (nuevoProducto) => {
    setProductos((prevProductos) => [...prevProductos, nuevoProducto]);
    manejarCerrarModalProducto();
  };

  // Simulación de carga inicial de datos (API calls)
  useEffect(() => {
    const cargarDatosIniciales = async () => {
      try {
        const responseProductos = await fetch(`${import.meta.env.VITE_API_BASE_URL}/productos`);
        const productosData = await responseProductos.json();
        setProductos(productosData);

        const responseMarcas = await fetch(`${import.meta.env.VITE_API_BASE_URL}/marcas`);
        const marcasData = await responseMarcas.json();
        setMarcas(marcasData);

        const responseCategorias = await fetch(`${import.meta.env.VITE_API_BASE_URL}/categorias`);
        const categoriasData = await responseCategorias.json();
        setCategorias(categoriasData);

        const responseProveedores = await fetch(`${import.meta.env.VITE_API_BASE_URL}/proveedores`);
        const proveedoresData = await responseProveedores.json();
        setProveedores(proveedoresData);

        const responseAlmacenes = await fetch(`${import.meta.env.VITE_API_BASE_URL}/almacenes`);
        const almacenesData = await responseAlmacenes.json();
        setAlmacenes(almacenesData);
      } catch (error) {
        console.error("Error al cargar datos iniciales:", error);
      }
    };

    cargarDatosIniciales();
  }, []);

  return (
    <div className="configuracion-panel">
      <h1>Panel de Configuración</h1>

      {/* Tabs de navegación */}
      <div className="tabs">
        <button
          onClick={() => setTabSeleccionada("TablaProductos")}
          className={tabSeleccionada === "TablaProductos" ? "active" : ""}
        >
          Productos
        </button>
        <button
          onClick={() => setTabSeleccionada("Marca")}
          className={tabSeleccionada === "Marca" ? "active" : ""}
        >
          Marcas
        </button>
        <button
          onClick={() => setTabSeleccionada("Categoria")}
          className={tabSeleccionada === "Categoria" ? "active" : ""}
        >
          Categorías
        </button>
        <button
          onClick={() => setTabSeleccionada("proveedores")}
          className={tabSeleccionada === "proveedores" ? "active" : ""}
        >
          Proveedores
        </button>
        <button
          onClick={() => setTabSeleccionada("Almacenes")}
          className={tabSeleccionada === "Almacenes" ? "active" : ""}
        >
          Almacenes
        </button>
      </div>

      {/* Contenido dinámico de las tabs */}
      <div className="tab-content">
        {tabSeleccionada === "TablaProductos" && (
          <div className="content">
            <div className="half">
              <button onClick={manejarAbrirModalProducto}>Agregar Producto</button>

              {modalProductoVisible && (
                <AgregarProducto
                  onProductoAgregado={manejarProductoAgregado}
                  onClose={manejarCerrarModalProducto}
                />
              )}
            </div>
            <div className="half">
              <TablaProductos productos={productos} />
            </div>
          </div>
        )}
        {tabSeleccionada === "Marca" && (
          <Marcas marcas={marcas} setMarcas={setMarcas} />
        )}
        {tabSeleccionada === "Categoria" && (
          <Categorias categorias={categorias} setCategorias={setCategorias} />
        )}
        {tabSeleccionada === "proveedores" && (
          <Proveedores proveedores={proveedores} setProveedores={setProveedores} />
        )}
        {tabSeleccionada === "Almacenes" && (
          <Almacenes almacenes={almacenes} setAlmacenes={setAlmacenes} />
        )}
      </div>
    </div>
  );
};

export default Config;
