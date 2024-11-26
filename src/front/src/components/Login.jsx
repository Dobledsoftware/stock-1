import { useState } from 'react';
import PropTypes from 'prop-types';
import '../styles/Login.css'; // Mantén tus estilos en este archivo

const Login = ({ onLogin }) => {
    const [cuil, setCuil] = useState('');
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [loginMethod, setLoginMethod] = useState('LDAP'); // Por defecto LDAP
    const [cuilError, setCuilError] = useState(false);
    const [isDisabled, setIsDisabled] = useState(true);
    const [error, setError] = useState(''); // Estado para manejar errores

    // Validación de CUIL
    const validateCuil = (value) => {
        const cuilPattern = /^[0-9]{11}$/;
        setCuilError(!cuilPattern.test(value));
        setCuil(value);
        checkFormValidity(value, password, loginMethod);
    };

    // Validación de formulario para habilitar botón
    const checkFormValidity = (identifier, password, method) => {
        if ((method === 'API' && identifier.length === 11 && password.length > 0) ||
            (method === 'LDAP' && identifier.length > 0 && password.length > 0)) {
            setIsDisabled(false);
        } else {
            setIsDisabled(true);
        }
    };

    const handlePasswordChange = (e) => {
        setPassword(e.target.value);
        checkFormValidity(loginMethod === 'API' ? cuil : username, e.target.value, loginMethod);
    };

    const handleLoginMethodChange = (e) => {
        setLoginMethod(e.target.value);
        // Reset fields when changing the method
        setCuil('');
        setUsername('');
        setPassword('');
        setIsDisabled(true);
        setError(''); // Resetear error al cambiar método
    };

    const handleUsernameChange = (e) => {
        setUsername(e.target.value);
        checkFormValidity(e.target.value, password, loginMethod);
    };

    // Lógica para manejar el login de acuerdo al método seleccionado
    const loginUsuario = async (e) => {
        e.preventDefault();
        setError(''); // Resetear el error

        try {
            let response;
            if (loginMethod === 'LDAP') {
                // Autenticación por LDAP
                response = await fetch('http://10.5.0.124:8000/login/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        samaccountname: username,
                        password: password,
                    }),
                });
            } else {
                // Autenticación por API
                response = await fetch('http://10.1.16.25:8085/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        cuil: cuil, // Aquí usamos el CUIL
                        password: password,
                    }),
                });
            }

            const data = await response.json();

            if (response.ok) {
                const { auth_token, nombre, apellido, cuil,email,legajo, Recibos } = data; // Acceder a los datos del usuario y recibos
                // Guardamos los datos del usuario en localStorage
                localStorage.setItem('auth_token', auth_token);
                localStorage.setItem('nombre', nombre);
                localStorage.setItem('apellido', apellido);
                localStorage.setItem('cuil', cuil);
                localStorage.setItem('email', email);
                localStorage.setItem('legajo', legajo);
                localStorage.setItem('recibos', JSON.stringify(Recibos));
                // Notificamos al componente padre que el login fue exitoso
                onLogin(auth_token);
            } else {
                // Manejo de errores
                setError(`Error en el login ${loginMethod}. Verifique sus credenciales.`);
            }
        // eslint-disable-next-line no-unused-vars
        } catch (error) {
            setError('Error de red o en el servidor.');
        }
    };

    return (
        <div className="login-wrapper">
            <div className="login-content">
                {/* Icono de información */}
                <a href="/manual/manual.pdf" target="_blank" className="info-icon" rel="noopener noreferrer">
                    <i className="fas fa-info-circle"></i>
                    <div className="tooltip">Manual de uso</div>
                </a>
                
                <div className="login-header">
                    <img src="/public/imgMail.png" alt="User Icon" className="user-icon" />
                    <h4>GesRe - HNAP</h4>
                    <h4>Inicio de sesión</h4>
                </div>

                {/* Selector de método de login */}
                <div>
                    <label htmlFor="login-method">Selecciona el método de autenticación:</label>
                    <select id="login-method" value={loginMethod} onChange={handleLoginMethodChange}>
                        <option value="LDAP">LDAP</option>
                        <option value="API">API</option>
                    </select>
                </div>

                {/* Formulario */}
                <form onSubmit={loginUsuario}>
                    {loginMethod === 'LDAP' ? (
                        <input
                            type="text"
                            value={username}
                            onChange={handleUsernameChange}
                            placeholder="samAccountName"
                            required
                        />
                    ) : (
                        <div>
                            <input
                                type="text"
                                value={cuil}
                                onChange={(e) => validateCuil(e.target.value)}
                                placeholder="Cuil"
                                required
                                maxLength="11"
                            />
                            {cuilError && <span className="error-text">El CUIL debe ser un número de 11 dígitos</span>}
                        </div>
                    )}
                    
                    <input
                        type="password"
                        value={password}
                        onChange={handlePasswordChange}
                        placeholder="Contraseña"
                        required
                    />
                    
                    {error && <span className="error-text">{error}</span>} {/* Mostrar errores */}

                    <input type="submit" value="Ingresar" disabled={isDisabled} />
                </form>

                <p>V 0.1.24</p>
                <p className="footer-text">Desarrollado por: Departamento de sistemas</p>
                <strong>Hospital Nac. Prof A. Posadas</strong>
            </div>
        </div>
    );
};

Login.propTypes = {
    onLogin: PropTypes.func.isRequired, // Marca el prop como requerido
};

export default Login;
