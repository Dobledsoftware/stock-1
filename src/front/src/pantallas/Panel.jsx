import React, { useEffect, useState } from 'react';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Typography, Grid } from '@mui/material';

function Panel() {
  const [minStockProducts, setMinStockProducts] = useState([]);
  const [lowStockProducts, setLowStockProducts] = useState([]);

  // Definir los umbrales
  const MIN_THRESHOLD = 10; // Stock mínimo
  const LOW_THRESHOLD = 5;  // Por agotarse

  // Simulación de productos
  const simulatedProducts = [
    { id: 1, name: 'Producto A', barcode: '123456', stock: 8 },
    { id: 2, name: 'Producto B', barcode: '234567', stock: 3 },
    { id: 3, name: 'Producto C', barcode: '345678', stock: 12 },
    { id: 4, name: 'Producto D', barcode: '456789', stock: 2 },
    { id: 5, name: 'Producto E', barcode: '567890', stock: 15 },
  ];

  useEffect(() => {
    // Simular la carga de productos
    const products = simulatedProducts;

    // Filtrar productos según los umbrales
    const minStock = products.filter((product) => product.stock <= MIN_THRESHOLD && product.stock > LOW_THRESHOLD);
    const lowStock = products.filter((product) => product.stock <= LOW_THRESHOLD);

    setMinStockProducts(minStock);
    setLowStockProducts(lowStock);
  }, []);

  return (
    <Grid container spacing={3} style={{ padding: 20 }}>
      <Grid item xs={12}>
        <Typography variant="h5" gutterBottom>
          Gestión de Stock
        </Typography>
      </Grid>

      {/* Tabla de Productos en el Mínimo */}
      <Grid item xs={12} md={6}>
        <Typography variant="h6" gutterBottom>
          Productos en el Mínimo
        </Typography>
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Producto</TableCell>
                <TableCell>Código de Barras</TableCell>
                <TableCell>Stock</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {minStockProducts.length > 0 ? (
                minStockProducts.map((product) => (
                  <TableRow key={product.id}>
                    <TableCell>{product.name}</TableCell>
                    <TableCell>{product.barcode}</TableCell>
                    <TableCell>{product.stock}</TableCell>
                  </TableRow>
                ))
              ) : (
                <TableRow>
                  <TableCell colSpan={3} align="center">
                    No hay productos en el mínimo.
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </TableContainer>
      </Grid>

      {/* Tabla de Productos por Agotarse */}
      <Grid item xs={12} md={6}>
        <Typography variant="h6" gutterBottom>
          Productos por Agotarse
        </Typography>
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Producto</TableCell>
                <TableCell>Código de Barras</TableCell>
                <TableCell>Stock</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {lowStockProducts.length > 0 ? (
                lowStockProducts.map((product) => (
                  <TableRow key={product.id}>
                    <TableCell>{product.name}</TableCell>
                    <TableCell>{product.barcode}</TableCell>
                    <TableCell>{product.stock}</TableCell>
                  </TableRow>
                ))
              ) : (
                <TableRow>
                  <TableCell colSpan={3} align="center">
                    No hay productos por agotarse.
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </TableContainer>
      </Grid>
    </Grid>
  );
}

export default Panel;
