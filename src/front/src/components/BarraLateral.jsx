import React, { useState } from 'react';
import { NavLink } from 'react-router-dom';
import { styled, useTheme } from '@mui/material/styles';
import MuiDrawer from '@mui/material/Drawer';
import List from '@mui/material/List';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import IconButton from '@mui/material/IconButton';
import Collapse from '@mui/material/Collapse';
import Divider from '@mui/material/Divider';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import MenuIcon from '@mui/icons-material/Menu';
import ChevronLeftIcon from '@mui/icons-material/ChevronLeft';
import ArchiveIcon from '@mui/icons-material/Archive';
import ShoppingCartIcon from '@mui/icons-material/ShoppingCart';
import SettingsIcon from '@mui/icons-material/Settings';
import PersonIcon from '@mui/icons-material/Person';
import ExitToAppIcon from '@mui/icons-material/ExitToApp';
import ExpandLess from '@mui/icons-material/ExpandLess';
import ExpandMore from '@mui/icons-material/ExpandMore';

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

const DrawerHeader = styled('div')(({ theme }) => ({
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  padding: theme.spacing(0, 1),
  ...theme.mixins.toolbar,
}));

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

  const toggleDrawer = () => {
    setOpen(!open);
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
        <ListItemButton onClick={() => {
          localStorage.removeItem('auth_token');
          localStorage.removeItem('usuario');
          window.location.href = "/"; // Redirigir sin recargar toda la app
        }}>
          <ListItemIcon><ExitToAppIcon /></ListItemIcon>
          {open && <ListItemText primary="Salir" />}
        </ListItemButton>
      </List>
    </Drawer>
  );
};

export default BarraLateral;
