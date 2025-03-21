import React, { useState } from 'react';
import { NavLink } from 'react-router-dom';
import { styled, useTheme } from '@mui/material/styles';
import MuiDrawer from '@mui/material/Drawer';
import List from '@mui/material/List';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import Divider from '@mui/material/Divider';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import ExitToAppIcon from '@mui/icons-material/ExitToApp';
import { Snackbar, Alert } from '@mui/material';
import ArchiveIcon from '@mui/icons-material/Archive';
import ShoppingCartIcon from '@mui/icons-material/ShoppingCart';
import SettingsIcon from '@mui/icons-material/Settings';
import PersonIcon from '@mui/icons-material/Person';

const drawerWidth = 240;

const openedMixin = (theme) => ({
  width: drawerWidth,
  transition: theme.transitions.create('width', {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.enteringScreen,
  }),
  overflowX: 'hidden',
});

const closedMixin = (theme) => ({
  transition: theme.transitions.create('width', {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.leavingScreen,
  }),
  overflowX: 'hidden',
  width: '70px',
  [theme.breakpoints.up('sm')]: {
    width: '70px',
  },
});

const Drawer = styled(MuiDrawer, {
  shouldForwardProp: (prop) => prop !== 'open',
})(({ theme, open }) => ({
  width: drawerWidth,
  flexShrink: 0,
  whiteSpace: 'nowrap',
  boxSizing: 'border-box',
  ...(open && {
    ...openedMixin(theme),
    '& .MuiDrawer-paper': openedMixin(theme),
  }),
  ...(!open && {
    ...closedMixin(theme),
    '& .MuiDrawer-paper': closedMixin(theme),
  }),
}));

const menuItems = [
  { id: 1, label: 'Productos', path: '/productos', icon: <ArchiveIcon /> },
  { id: 2, label: 'Ventas', path: '/ventas', icon: <ShoppingCartIcon /> },
  { id: 3, label: 'Administración', path: '/administracion', icon: <SettingsIcon /> },
  { id: 4, label: 'Panel', path: '/panel', icon: <PersonIcon /> },
  { id: 5, label: 'Abastecimiento', path: '/abastecimiento', icon: <ArchiveIcon /> },
  { id: 6, label: 'Cierre de Caja', path: '/cierre', icon: <ShoppingCartIcon /> },
  { id: 7, label: 'Configuración', path: '/configuracion', icon: <SettingsIcon /> },
  { id: 8, label: 'Config Stock', path: '/config', icon: <ArchiveIcon /> },
  { id: 9, label: 'Movimientos Stock', path: '/movimientos', icon: <ArchiveIcon /> },
  { id: 10, label: 'Inventario', path: '/inventario', icon: <ArchiveIcon /> },
];

const BarraLateral = ({ permisosUsuario }) => {
  const theme = useTheme();
  const [open, setOpen] = useState(true);
  const [logoutSnackbar, setLogoutSnackbar] = useState(false);
  const [errorSnackbar, setErrorSnackbar] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  const toggleDrawer = () => {
    setOpen(!open);
  };

  const handleLogout = async () => {
    const authToken = localStorage.getItem('auth_token');

    if (!authToken) {
      console.error("Error: No hay token de autenticación para cerrar sesión");
      setErrorMessage("No hay token de autenticación");
      setErrorSnackbar(true);
      return;
    }

    console.log("Enviando solicitud de logout con token:", authToken);

    try {
      const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/logout`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${authToken}`
        },
        body: JSON.stringify({})
      });

      const responseData = await response.json();
      console.log("Respuesta del servidor en logout:", response.status, responseData);

      if (!response.ok) {
        console.error("Error al cerrar sesión", response.status, responseData);
        setErrorMessage(responseData.detail || "Error al cerrar sesión");
        setErrorSnackbar(true);
        return;
      }

      console.log("Logout exitoso. Eliminando datos de sesión...");
      localStorage.removeItem('auth_token');
      localStorage.removeItem('usuario');
      setLogoutSnackbar(true);
      setTimeout(() => {
        window.location.href = "/";
      }, 2000);
    } catch (error) {
      console.error("Error en la solicitud de logout", error);
      setErrorMessage("Error de conexión con el servidor");
      setErrorSnackbar(true);
    }
  };

  return (
    <Drawer variant="permanent" open={open}>
      <Toolbar>
        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', width: '100%' }}>
          <img
            src="/img/imagen.jpg"
            alt="logo"
            style={{ maxWidth: open ? '180px' : '50px', cursor: 'pointer', transition: 'max-width 0.3s ease' }}
            onClick={toggleDrawer}
          />
        </Box>
      </Toolbar>
      <Divider />
      <List>
        {menuItems.filter(item => permisosUsuario.includes(item.id)).map(({ id, label, path, icon }) => (
          <ListItemButton key={id} component={NavLink} to={path}>
            <ListItemIcon>{icon}</ListItemIcon>
            {open && <ListItemText primary={label} />}
          </ListItemButton>
        ))}
      </List>
      <Divider />
      <List>
        <ListItemButton onClick={handleLogout}>
          <ListItemIcon><ExitToAppIcon /></ListItemIcon>
          {open && <ListItemText primary="Salir" />}
        </ListItemButton>
      </List>
      <Snackbar open={logoutSnackbar} autoHideDuration={2000} onClose={() => setLogoutSnackbar(false)}>
        <Alert onClose={() => setLogoutSnackbar(false)} severity="success" sx={{ width: '100%' }}>
          ¡Sesión cerrada con éxito!
        </Alert>
      </Snackbar>
    </Drawer>
  );
};

export default BarraLateral;