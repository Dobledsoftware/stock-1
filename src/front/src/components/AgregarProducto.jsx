import React, { useState } from 'react';
import PropTypes from 'prop-types';
import '../styles/AgregarProducto.css';  // Asegúrate de incluir los estilos necesarios

const AgregarProducto = ({ onProductoAgregado, onClose }) => {
    const [nombre, setNombre] = useState('');
    const [descripcion, setDescripcion] = useState('');
    const [precio, setPrecio] = useState('');
    const [marca, setMarca] = useState('');
    const [id_categoria, setIdCategoria] = useState('');
    const [codigo_barras, setCodigoBarras] = useState('');
    //const [imagen, setImagen] = useState(null);  // Para almacenar la imagen seleccionada

    const [mensaje, setMensaje] = useState('');
    const [error, setError] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();

        // Asumir que no se está utilizando imagen por ahora
        // const imagenProductoUrl = imagen ? `https://drive.google.com/uc?id=${imagen}` : '';  // URL de la imagen

        const nuevoProducto = {
            accion: 'agregarProducto',
            nombre,
            descripcion,
            precio: parseFloat(precio),
            marca,
            id_categoria: parseFloat(id_categoria),
            codigo_barras,
            //imagen_producto: imagenProductoUrl, // Aquí agregas la URL de la imagen (comentado por ahora)
            forceAdd: false
        };

        try {
            const formData = new FormData();
            formData.append('producto', JSON.stringify(nuevoProducto));

            // Si tienes la imagen en un archivo y necesitas enviarla (comentado por ahora)
            /* if (imagen) {
                formData.append('imagen_producto', imagen); // Agregar la imagen como archivo
            } */

            const response = await fetch(`
                ${import.meta.env.VITE_API_BASE_URL}/producto`, {
                method: 'POST',
                body: formData,
            });

            if (response.ok) {
                const data = await response.json();
                setMensaje(`Producto '${data.message}' agregado exitosamente.`);
                setError('');
                onProductoAgregado(data);
                onClose(); // Cerrar el modal al agregar el producto
                setNombre('');
                setDescripcion('');
                setPrecio('');
                setIdCategoria('');
                setCodigoBarras('');
                setMarca('');
                //setImagen(null); // Resetear la imagen seleccionada (comentado por ahora)
            } else {
                const errorData = await response.json();
                if (errorData.status === 'warning') {
                    setMensaje('');
                    setError(`Advertencia: ${errorData.message}`);
                } else {
                    throw new Error(errorData.message || 'Error al agregar el producto');
                }
            }
        } catch (error) {
            setError(`Error: ${error.message}`);
            setMensaje('');
        }
    };

    // El código para manejar la imagen ha sido comentado por ahora
    /* const handleImageChange = (e) => {
        const file = e.target.files[0];
        if (file) {
            setImagen(file);  // Guardar la imagen seleccionada
        }
    }; */

    return (
        <div className="modal">
            <div className="modal-content">
                <span className="close" onClick={onClose}>&times;</span>
                <h2>Agregar Producto</h2>
                <form onSubmit={handleSubmit}>
                    <input
                        type="text"
                        placeholder="Nombre"
                        value={nombre}
                        onChange={(e) => setNombre(e.target.value)}
                        required
                    />
                    <input
                        type="text"
                        placeholder="Descripción"
                        value={descripcion}
                        onChange={(e) => setDescripcion(e.target.value)}
                        required
                    />
                    <input
                        type="number"
                        placeholder="Precio"
                        value={precio}
                        onChange={(e) => setPrecio(e.target.value)}
                        required
                    />
                    <input
                        type="number"
                        placeholder="Categoría"
                        value={id_categoria}
                        onChange={(e) => setIdCategoria(e.target.value)}
                        required
                    />
                    <input
                        type="text"
                        placeholder="Marca"
                        value={marca}
                        onChange={(e) => setMarca(e.target.value)}
                        required
                    />
                    <input
                        type="text"
                        placeholder="Código de Barras"
                        value={codigo_barras}
                        onChange={(e) => setCodigoBarras(e.target.value)}
                        required
                    />
                    {/* Aquí va el componente de imagen que hemos comentado por ahora */}
                    {/* <div className="file-input-container">
                        <input
                            type="file"
                            onChange={handleImageChange}
                            accept="image/*"
                        />
                        {imagen && <p>Imagen seleccionada: {imagen.name}</p>}
                    </div> */}
                    <button type="submit">Agregar Producto</button>
                </form>

                {mensaje && <p className="mensaje-exito">{mensaje}</p>}
                {error && <p className="mensaje-error">{error}</p>}
            </div>
        </div>
    );
};

AgregarProducto.propTypes = {
    onProductoAgregado: PropTypes.func.isRequired,
    onClose: PropTypes.func.isRequired,
};

export default AgregarProducto;
