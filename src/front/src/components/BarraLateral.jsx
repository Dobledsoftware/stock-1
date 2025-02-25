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

// Íconos de Material UI para cada sección
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
  width: '70px', // Ancho cuando la barra está "cerrada"
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

// Configuración del Drawer para manejar los estados abierto/cerrado
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

const BarraLateral = () => {
  const theme = useTheme();
  const [open, setOpen] = useState(true);
  const [activeItem, setActiveItem] = useState('');

  // Alterna el estado del Drawer (abierto/cerrado)
  const toggleDrawer = () => {
    setOpen(!open);
  };

  // Alterna el submenú activo y, si está cerrado, abre la barra
  const handleActiveItem = (item) => {
    setActiveItem(activeItem === item ? '' : item);
    if (!open) {
      setOpen(true);
    }
  };

  return (
    <Drawer variant="permanent" open={open}>
      <Toolbar>
        <Box
          sx={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            width: '100%',
          }}
        >
          {/* Logo con función para alternar el Drawer */}
          <img
            src="/img/imagen.jpg"
            alt="logo"
            style={{
              maxWidth: open ? '180px' : '50px',
              cursor: 'pointer',
              transition: 'max-width 0.3s ease',
            }}
            onClick={toggleDrawer}
          />
        </Box>
      </Toolbar>
      <Divider />
      <List>
        {/* Menú Stock */}
        <ListItemButton onClick={() => handleActiveItem('stock')}>
          <ListItemIcon>
            <ArchiveIcon />
          </ListItemIcon>
          {open && <ListItemText primary="Stock" />}
          {open && (activeItem === 'stock' ? <ExpandLess /> : <ExpandMore />)}
        </ListItemButton>
        <Collapse in={activeItem === 'stock' && open} timeout="auto" unmountOnExit>
          <List component="div" disablePadding>
            <ListItemButton sx={{ pl: 4 }} component={NavLink} to="/inventario">
              <ListItemText primary="Inventario" />
            </ListItemButton>
            <ListItemButton sx={{ pl: 4 }} component={NavLink} to="/movimientos">
              <ListItemText primary="Stock" />
            </ListItemButton>
            <ListItemButton sx={{ pl: 4 }} component={NavLink} to="/config">
              <ListItemText primary="Panel de configuración stock" />
            </ListItemButton>
            <ListItemButton sx={{ pl: 4 }} component={NavLink} to="/abastecimiento">
              <ListItemText primary="Abastecimiento" />
            </ListItemButton>
            <ListItemButton sx={{ pl: 4 }} component={NavLink} to="/panel">
              <ListItemText primary="Panel" />
            </ListItemButton>
          </List>
        </Collapse>

        {/* Menú Ventas */}
        <ListItemButton onClick={() => handleActiveItem('ventas')}>
          <ListItemIcon>
            <ShoppingCartIcon />
          </ListItemIcon>
          {open && <ListItemText primary="Ventas" />}
          {open && (activeItem === 'ventas' ? <ExpandLess /> : <ExpandMore />)}
        </ListItemButton>
        <Collapse in={activeItem === 'ventas' && open} timeout="auto" unmountOnExit>
          <List component="div" disablePadding>
            <ListItemButton sx={{ pl: 4 }} component={NavLink} to="/ventas">
              <ListItemText primary="Nueva Venta" />
            </ListItemButton>
            <ListItemButton sx={{ pl: 4 }} component={NavLink} to="/cierre">
              <ListItemText primary="Cierre de Caja" />
            </ListItemButton>
          </List>
        </Collapse>

        {/* Menú Administración */}
        <ListItemButton onClick={() => handleActiveItem('administracion')}>
          <ListItemIcon>
            <SettingsIcon />
          </ListItemIcon>
          {open && <ListItemText primary="Administración" />}
          {open && (activeItem === 'administracion' ? <ExpandLess /> : <ExpandMore />)}
        </ListItemButton>
        <Collapse in={activeItem === 'administracion' && open} timeout="auto" unmountOnExit>
          <List component="div" disablePadding>
            <ListItemButton sx={{ pl: 4 }} component={NavLink} to="/administracion">
              <ListItemText primary="Usuarios" />
            </ListItemButton>
            <ListItemButton sx={{ pl: 4 }} component={NavLink} to="/configuracion">
              <ListItemText primary="Configuración" />
            </ListItemButton>
          </List>
        </Collapse>

        {/* Menú Perfil */}
        <ListItemButton onClick={() => handleActiveItem('perfil')}>
          <ListItemIcon>
            <PersonIcon />
          </ListItemIcon>
          {open && <ListItemText primary="Perfil" />}
          {open && (activeItem === 'perfil' ? <ExpandLess /> : <ExpandMore />)}
        </ListItemButton>
        <Collapse in={activeItem === 'perfil' && open} timeout="auto" unmountOnExit>
          <List component="div" disablePadding>
            <ListItemButton sx={{ pl: 4 }} component={NavLink} to="/editar-perfil">
              <ListItemText primary="Editar Perfil" />
            </ListItemButton>
            <ListItemButton sx={{ pl: 4 }} component={NavLink} to="/cambiar-contrasena">
              <ListItemText primary="Cambiar Contraseña" />
            </ListItemButton>
          </List>
        </Collapse>

        {/* Opción Salir */}
        <ListItemButton>
          <ListItemIcon>
            <ExitToAppIcon />
          </ListItemIcon>
          {open && <ListItemText primary="Salir" />}
        </ListItemButton>
      </List>
    </Drawer>
  );
};

export default BarraLateral;
