import { useState } from 'react';
import PropTypes from 'prop-types';
import '../styles/Login.css';

const Login = ({ onLogin }) => {
    const [cuil, setCuil] = useState('');
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [loginMethod, setLoginMethod] = useState('LDAP');
    const [cuilError, setCuilError] = useState(false);
    const [isDisabled, setIsDisabled] = useState(true);
    const [error, setError] = useState('');

    const validateCuil = (value) => {
        const cuilPattern = /^[0-9]{11}$/;
        setCuilError(!cuilPattern.test(value));
        setCuil(value);
        checkFormValidity(value, password, loginMethod);
    };

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
        setCuil('');
        setUsername('');
        setPassword('');
        setIsDisabled(true);
        setError('');
    };

    const handleUsernameChange = (e) => {
        setUsername(e.target.value);
        checkFormValidity(e.target.value, password, loginMethod);
    };

    // Función para almacenar datos en localStorage
    const storeUserData = (data) => {
        localStorage.setItem('auth_token', data.auth_token);
        localStorage.setItem('nombre', data.nombre || '');
        localStorage.setItem('apellido', data.apellido || '');
        localStorage.setItem('cuil', data.cuil || '');
        localStorage.setItem('email', data.email || '');
        localStorage.setItem('legajo', data.legajo || '');
        localStorage.setItem('rol', data.rol || '');
        localStorage.setItem('recibos', JSON.stringify(data.Recibos || []));

        onLogin(data.auth_token);
    };

    // Lógica para manejar el login de acuerdo al método seleccionado
    const loginUsuario = async (e) => {
        e.preventDefault();
        setError('');

        try {
            if (loginMethod === 'LDAP') {
                const ldapResponse = await fetch(`${import.meta.env.VITE_LDAP_API}/login/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        samaccountname: username,
                        password: password,
                    }),
                });

                const ldapData = await ldapResponse.json();

                if (ldapResponse.ok && ldapData.auth_token) {
                    const authToken = ldapData.auth_token;

                    // Obtiene el JSON completo del rol
                    const roleResponse = await fetch(`${import.meta.env.VITE_API_BASE_URL}/get_rol`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ token: authToken }),
                    });

                    const roleData = await roleResponse.json();

                    if (roleResponse.ok) {
                        // Llamada a storeUserData con el JSON obtenido de get_rol
                        storeUserData(roleData);
                    } else {
                        setError('No se pudo obtener el rol del usuario.');
                        console.error("Error obteniendo rol del usuario", roleData);
                    }
                } else {
                    setError('Error en el login LDAP. Verifique sus credenciales.');
                    console.error("Error en la autenticación LDAP", ldapData);
                }

            } else {
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
                } else {
                    setError('Error en el login API. Verifique sus credenciales.');
                    console.error("Error en autenticación API", apiData);
                }
            }
        } catch (error) {
            setError('Error de red o en el servidor.');
            console.error("Error de red o servidor", error);
        }
    };

    return (
        <div className="login-wrapper">
            <div className="login-content">
                <a href="/manual/manual.pdf" target="_blank" className="info-icon" rel="noopener noreferrer">
                    <i className="fas fa-info-circle"></i>
                    <div className="tooltip">Manual de uso</div>
                </a>

                <div className="login-header">
                    <img src="/public/img/imgMail.png" alt="User Icon" className="user-icon" />
                    <h4>GesRe - HNAP</h4>
                    <h4>Inicio de sesión</h4>
                </div>

                <div>
                    <label htmlFor="login-method">Selecciona el método de autenticación:</label>
                    <select id="login-method" value={loginMethod} onChange={handleLoginMethodChange}>
                        <option value="LDAP">Usuario de windows</option>
                        <option value="API">Usuario de Recibo de sueldo</option>
                    </select>
                </div>

                <form onSubmit={loginUsuario}>
                    {loginMethod === 'LDAP' ? (
                        <input
                            type="text"
                            value={username}
                            onChange={handleUsernameChange}
                            placeholder="Dni"
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

                    {error && <span className="error-text">{error}</span>}

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
    onLogin: PropTypes.func.isRequired,
};

export default Login;
