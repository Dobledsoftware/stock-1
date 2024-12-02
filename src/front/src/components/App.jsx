import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { FaBars, FaTimes } from 'react-icons/fa'; // Importamos los iconos de react-icons
import Login from './Login';
import Stock from '../paginas/stock';
import Ventas from '../paginas/ventas';
import Header from './Header';
import Sidebar from './Sidebar'; // Importa el Sidebar

const App = () => {
    const [userRole, setUserRole] = useState(null);
    const [sidebarVisible, setSidebarVisible] = useState(true); // Estado para controlar la visibilidad del Sidebar

    useEffect(() => {
        // Obtener el rol del usuario desde localStorage
        const role = localStorage.getItem('rol');
        if (role) {
            setUserRole(role);
        }
    }, []);

    const handleLogin = (token) => {
        // Aquí puedes usar el token para hacer cualquier cosa que necesites (como guardarlo)
        console.log('Usuario logueado con token: ', token);
    };

    const toggleSidebar = () => {
        setSidebarVisible(!sidebarVisible); // Cambia el estado del Sidebar
    };

    if (!userRole) {
        return (
            <Router>
                <Routes>
                    <Route path="/" element={<Login onLogin={handleLogin} />} />
                    <Route path="*" element={<Navigate to="/" />} />
                </Routes>
            </Router>
        );
    }

    return (
        <Router>
            <div className="main-layout">
                <Header /> {/* Header en la parte superior */}
                <div className="content-container">
                    <Sidebar sidebarVisible={sidebarVisible} toggleSidebar={toggleSidebar} /> {/* Sidebar con control de visibilidad */}
                    <div className={`content ${sidebarVisible ? '' : 'sidebar-hidden'}`}>
                        <Routes>
                            {userRole === 'admin' && <Route path="/stock" element={<Stock />} />}
                            <Route path="/ventas" element={<Ventas />} />
                            <Route path="*" element={<Navigate to="/ventas" />} />
                        </Routes>
                    </div>
                </div>
            </div>
        </Router>
    );
};

export default App;
