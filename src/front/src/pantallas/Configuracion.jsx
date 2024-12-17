import React, { useState, useEffect } from 'react';
import '../styles/configuracion.css';

const Configuracion = () => {
    const [tabSeleccionada, setTabSeleccionada] = useState('general');

    // Estado para configuraciones generales
    const [nombreApp, setNombreApp] = useState('');
    const [logoApp, setLogoApp] = useState('');
    const [iva, setIva] = useState(21); // Valor del IVA
    const [limiteStock, setLimiteStock] = useState(10);

    // Cargar configuraciones guardadas al montar el componente
    useEffect(() => {
        // Simular carga desde la API
        const cargarConfiguracion = async () => {
            // Simulación de datos guardados
            const configGuardada = {
                nombreApp: 'Mi Aplicación',
                logoApp: '',
                iva: 21,
                limiteStock: 10,
            };

            setNombreApp(configGuardada.nombreApp);
            setLogoApp(configGuardada.logoApp);
            setIva(configGuardada.iva);
            setLimiteStock(configGuardada.limiteStock);
        };

        cargarConfiguracion();
    }, []);

    // Guardar configuración en la base de datos
    const guardarConfiguracion = () => {
        const configuracion = {
            nombreApp,
            logoApp,
            iva,
            limiteStock,
        };

        console.log('Configuración guardada:', configuracion);
        alert('Configuración guardada correctamente');
        // Aquí deberías realizar la llamada al backend con fetch/axios
    };

    return (
        <div className="configuracion-panel">
            <h1>Panel de Configuración</h1>

            {/* Navegación entre pestañas */}
            <div className="tabs">
                <button
                    onClick={() => setTabSeleccionada('general')}
                    className={tabSeleccionada === 'general' ? 'active' : ''}
                >
                    Configuración General
                </button>
                <button
                    onClick={() => setTabSeleccionada('parametros')}
                    className={tabSeleccionada === 'parametros' ? 'active' : ''}
                >
                    Parámetros
                </button>
                <button
                    onClick={() => setTabSeleccionada('usuarios')}
                    className={tabSeleccionada === 'usuarios' ? 'active' : ''}
                >
                    Gestión de Usuarios
                </button>
            </div>

            {/* Contenido de la pestaña */}
            <div className="tab-content">
                {tabSeleccionada === 'general' && (
                    <div className="tab-general">
                        <h2>Configuración General</h2>
                        <div className="form-group">
                            <label>Nombre de la Aplicación:</label>
                            <input
                                type="text"
                                value={nombreApp}
                                onChange={(e) => setNombreApp(e.target.value)}
                            />
                        </div>
                        <div className="form-group">
                            <label>Logo de la Aplicación:</label>
                            <input
                                type="file"
                                onChange={(e) => setLogoApp(e.target.files[0])}
                            />
                        </div>
                    </div>
                )}

                {tabSeleccionada === 'parametros' && (
                    <div className="tab-parametros">
                        <h2>Configuración de Parámetros</h2>
                        <div className="form-group">
                            <label>IVA (%):</label>
                            <input
                                type="number"
                                value={iva}
                                onChange={(e) => setIva(parseFloat(e.target.value))}
                            />
                        </div>
                        <div className="form-group">
                            <label>Límite de Stock:</label>
                            <input
                                type="number"
                                value={limiteStock}
                                onChange={(e) =>
                                    setLimiteStock(parseInt(e.target.value))
                                }
                            />
                        </div>
                    </div>
                )}

                {tabSeleccionada === 'usuarios' && (
                    <div className="tab-usuarios">
                        <h2>Gestión de Perfiles</h2>
                        <p>Aquí podrás crear, editar y eliminar perfiles (Próximamente).</p>
                    </div>
                )}
            </div>

            {/* Botón de Guardar Configuración */}
            <div className="guardar-configuracion">
                <button onClick={guardarConfiguracion}>Guardar Configuración</button>
            </div>
        </div>
    );
};

export default Configuracion;
