import { useState } from 'react';
import PropTypes from 'prop-types';
import { useNavigate } from 'react-router-dom';
import { Snackbar, Alert } from '@mui/material';
import '../styles/Login.css';

const Login = ({ onLogin }) => {
    const [usuario, setUsuario] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [successSnackbar, setSuccessSnackbar] = useState(false);
    const [errorSnackbar, setErrorSnackbar] = useState(false);
    const [errorMessage, setErrorMessage] = useState('');
    const navigate = useNavigate();

    const handleUsuarioChange = (e) => {
        setUsuario(e.target.value);
    };

    const handlePasswordChange = (e) => {
        setPassword(e.target.value);
    };

    const loginUsuario = async (e) => {
        e.preventDefault();
        setError('');

        if (!usuario || !password) {
            setError('Usuario y contraseña son obligatorios.');
            setErrorMessage('Usuario y contraseña son obligatorios.');
            setErrorSnackbar(true);
            return;
        }

        try {
            const apiResponse = await fetch(`${import.meta.env.VITE_API_BASE_URL}/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ usuario, password }),
            });

            const apiData = await apiResponse.json();
            console.log("Datos obtenidos de la API", apiData);

            if (!apiResponse.ok || typeof apiData.auth_token !== 'string') {
                setError(apiData.message || 'Error en el login. Verifique sus credenciales.');
                setErrorMessage(apiData.message || 'Error en el login.');
                setErrorSnackbar(true);
                return;
            }

            if (apiData.auth_token.startsWith("Sesión ya iniciada")) {
                setErrorMessage("Sesión ya iniciada, tiempo de expiración actualizado.");
                setErrorSnackbar(true);
                return;
            }

            setSuccessSnackbar(true);
            setTimeout(() => {
                onLogin(apiData.auth_token, apiData);
            }, 1500);
        } catch (error) {
            console.error("Error en la conexión con la API", error);
            setErrorMessage('Error de red o en el servidor.');
            setErrorSnackbar(true);
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
                    <input
                        type="text"
                        value={usuario}
                        onChange={handleUsuarioChange}
                        placeholder="Usuario"
                        required
                    />
                    <input
                        type="password"
                        value={password}
                        onChange={handlePasswordChange}
                        placeholder="Contraseña"
                        required
                    />
                    {error && <span className="error-text">{error}</span>}
                    <input type="submit" value="Ingresar" />
                </form>

                <p>V 0.1.24</p>
                <p className="footer-text">Desarrollado por: DDSOFTWARE 2025</p>
            </div>
            <Snackbar open={successSnackbar} autoHideDuration={3000} onClose={() => setSuccessSnackbar(false)}>
                <Alert onClose={() => setSuccessSnackbar(false)} severity="success" sx={{ width: '100%' }}>
                    ¡Inicio de sesión exitoso!
                </Alert>
            </Snackbar>
            <Snackbar open={errorSnackbar} autoHideDuration={3000} onClose={() => setErrorSnackbar(false)}>
                <Alert onClose={() => setErrorSnackbar(false)} severity="error" sx={{ width: '100%' }}>
                    {errorMessage}
                </Alert>
            </Snackbar>
        </div>
    );
};

Login.propTypes = {
    onLogin: PropTypes.func.isRequired,
};

export default Login;