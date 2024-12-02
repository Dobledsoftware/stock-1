import { useState } from 'react';
import PropTypes from 'prop-types';
import { useNavigate } from 'react-router-dom';  // Importa useNavigate
import '../styles/Login.css';

const Login = ({ onLogin }) => {
    const [cuil, setCuil] = useState('');
    const [password, setPassword] = useState('');
    const [cuilError, setCuilError] = useState(false);
    const [isDisabled, setIsDisabled] = useState(true);
    const [error, setError] = useState('');
    const navigate = useNavigate();  // Hook de navegación

    const validateCuil = (value) => {
        const cuilPattern = /^[0-9]{11}$/;
        setCuilError(!cuilPattern.test(value));
        setCuil(value);
        checkFormValidity(value, password);
    };

    const checkFormValidity = (cuil, password) => {
        if (cuil.length === 11 && password.length > 0) {
            setIsDisabled(false);
        } else {
            setIsDisabled(true);
        }
    };

    const handlePasswordChange = (e) => {
        setPassword(e.target.value);
        checkFormValidity(cuil, e.target.value);
    };

    const storeUserData = (data) => {
        localStorage.setItem('auth_token', data.auth_token);
        localStorage.setItem('nombre', data.nombre || '');
        localStorage.setItem('apellido', data.apellido || '');
        localStorage.setItem('cuil', data.cuil || '');
        localStorage.setItem('email', data.email || '');
        localStorage.setItem('rol', data.rol || '');
       
        onLogin(data.auth_token);
    };

    const loginUsuario = async (e) => {
        e.preventDefault();
        setError('');

        try {
            const apiResponse = await fetch(`${import.meta.env.VITE_API_BASE_URL}/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    cuil: cuil,
                    password: password,
                }),
            });

            const apiData = await apiResponse.json();

            if (apiResponse.ok) {
                storeUserData(apiData);
                // Redirige al usuario después de login
                navigate('/dashboard');  // Aquí va la ruta después del login
            } else {
                setError('Error en el login. Verifique sus credenciales.');
                console.error("Error en autenticación API", apiData);
            }
        } catch (error) {
            setError('Error de red o en el servidor.');
            console.error("Error de red o servidor", error);
        }
    };

    return (
        <div className="login-wrapper">
            <div className="login-content">
                <div className="login-header">
                    <img src="/public/img/imagen.jpg" alt="User Icon" className="user-icon" />
                    <h4>Legendary</h4>
                    <h4>Inicio de sesión</h4>
                </div>

                <form onSubmit={loginUsuario}>
                    <div>
                        <input
                            type="text"
                            value={cuil}
                            onChange={(e) => validateCuil(e.target.value)}
                            placeholder="CUIL"
                            required
                            maxLength="11"
                        />
                        {cuilError && <span className="error-text">El CUIL debe ser un número de 11 dígitos</span>}
                    </div>

                    <input
                        type="password"
                        value={password}
                        onChange={handlePasswordChange}
                        placeholder="Contraseña"
                        required
                    />

                    {error && <span className="error-text">{error}</span>}

                    <input type="submit" value="Ingresar" disabled={isDisabled} />
                </form>

                <p>V 0.1.24</p>
                <p className="footer-text">Desarrollado por: DDSOFTWARE 2025</p>
            </div>
        </div>
    );
};

Login.propTypes = {
    onLogin: PropTypes.func.isRequired,
};

export default Login;
