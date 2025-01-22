import React from 'react';

const ProductosSeleccionados = ({ productos, onEliminarProducto }) => {
    return (
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '10px' }}>
            {productos.map((producto) => (
                <div
                    key={producto.id_producto}
                    style={{
                        display: 'flex',
                        alignItems: 'center',
                        backgroundColor: '#f0f0f0',
                        padding: '5px 10px',
                        borderRadius: '20px',
                    }}
                >
                    <span>{producto.producto_nombre}</span>
                    <button
                        onClick={() => onEliminarProducto(producto.id_producto)}
                        style={{
                            marginLeft: '5px',
                            background: 'none',
                            border: 'none',
                            cursor: 'pointer',
                        }}
                    >
                        &times;
                    </button>
                </div>
            ))}
        </div>
    );
};

export default ProductosSeleccionados;
