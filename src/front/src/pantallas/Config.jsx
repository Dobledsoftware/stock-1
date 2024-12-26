import React, { useState, useEffect } from 'react';
import Categorias from '../components/Categorias';
import Marcas from '../components/Marcas'; // Importar el componente de marcas
import Proveedores from '../components/Proveedores'; // Importar el componente de proveedores
import Almacenes from '../components/Almacen'; // Importar el componente de proveedores
import '../styles/configuracion.css';

const Config = () => {
    const [tabSeleccionada, setTabSeleccionada] = useState('general');

    useEffect(() => {
        const cargarConfiguracion = async () => {
            console.log('Cargando configuraciones iniciales...');
        };

        cargarConfiguracion();
    }, []);

    return (
        <div className="configuracion-panel">
            <h1>Panel de Configuración de los productos</h1>

            <div className="tabs">
                <button
                    onClick={() => setTabSeleccionada('Marca')}
                    className={tabSeleccionada === 'Marca' ? 'active' : ''}
                >
                    Marcas
                </button>
                <button
                    onClick={() => setTabSeleccionada('Categoria')}
                    className={tabSeleccionada === 'Categoria' ? 'active' : ''}
                >
                    Categorias
                </button>
                <button
                    onClick={() => setTabSeleccionada('proveedores')}
                    className={tabSeleccionada === 'proveedores' ? 'active' : ''}
                >
                    Proveedores
                </button>
                <button
                    onClick={() => setTabSeleccionada('Almacenes')}
                    className={tabSeleccionada === 'Almacenes' ? 'active' : ''}
                >
                    Almacenes
                </button>
               
            </div>

            <div className="tab-content">
                {tabSeleccionada === 'Marca' && (
                    <Marcas apiBaseUrl={import.meta.env.VITE_API_BASE_URL} />
                )}
                {tabSeleccionada === 'Categoria' && (
                    <Categorias apiBaseUrl={import.meta.env.VITE_API_BASE_URL} />
                )}
                {tabSeleccionada === 'proveedores' && (
                    <Proveedores apiBaseUrl={import.meta.env.VITE_API_BASE_URL} />
                )}
                {tabSeleccionada === 'Almacenes' && (
                    <Almacenes apiBaseUrl={import.meta.env.VITE_API_BASE_URL} />
                )}
               
            </div>
        </div>
    );
};

export default Config;
