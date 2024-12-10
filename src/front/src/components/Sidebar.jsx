import React from 'react';
import { Link } from 'react-router-dom';
import { FaHome, FaBox, FaShoppingCart } from 'react-icons/fa';
import '../styles/Sidebar.css';

const Sidebar = ({ sidebarVisible, toggleSidebar }) => {
    return (
        <div className={`sidebar ${sidebarVisible ? 'sidebar-visible' : 'sidebar-hidden'}`}>
            <button className="sidebar-toggle" onClick={toggleSidebar}>
                {sidebarVisible ? (
                    <span>&lt;</span> // Icono para ocultar
                ) : (
                    <span>&gt;</span> // Icono para mostrar
                )}
            </button>
            <div className="sidebar-nav">
                <ul>
                    <li>
                        <Link to="/ventas">
                            <FaShoppingCart />
                            {sidebarVisible && <span>Ventas</span>}
                        </Link>
                    </li>
                    <li>
                        <Link to="/stock">
                            <FaBox />
                            {sidebarVisible && <span>Stock</span>}
                        </Link>
                    </li>
                    <li>
                        <Link to="/home">
                            <FaHome />
                            {sidebarVisible && <span>Home</span>}
                        </Link>
                    </li>
                </ul>
            </div>
        </div>
    );
};

export default Sidebar;
