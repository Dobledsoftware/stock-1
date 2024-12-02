import React from 'react';
import { Link } from 'react-router-dom';
import { FaHome, FaBox, FaShoppingCart, FaBars, FaTimes } from 'react-icons/fa'; // Importa los iconos de react-icons
import '../styles/Sidebar.css';

const Sidebar = ({ sidebarVisible, toggleSidebar }) => {
    return (
        <div className={`sidebar ${sidebarVisible ? 'sidebar-visible' : 'sidebar-hidden'}`}>
            <button className="sidebar-toggle" onClick={toggleSidebar}>
                {sidebarVisible ? (
                    <FaTimes /> // Icono para ocultar el sidebar
                ) : (
                    <FaBars /> // Icono para mostrar el sidebar
                )}
            </button>
            <div className="sidebar-nav">
                <ul>
                    <li>
                        <Link to="/ventas">
                            <FaShoppingCart />
                            {sidebarVisible && <span>Ventas</span>} {/* Mostrar solo el texto cuando el sidebar está visible */}
                        </Link>
                    </li>
                    <li>
                        <Link to="/stock">
                            <FaBox />
                            {sidebarVisible && <span>Stock</span>} {/* Mostrar solo el texto cuando el sidebar está visible */}
                        </Link>
                    </li>
                    <li>
                        <Link to="/home">
                            <FaHome />
                            {sidebarVisible && <span>Home</span>} {/* Mostrar solo el texto cuando el sidebar está visible */}
                        </Link>
                    </li>
                </ul>
            </div>
        </div>
    );
};

export default Sidebar;
