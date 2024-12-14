import React, { useEffect, useState } from 'react';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Typography, Grid } from '@mui/material';
import axios from 'axios';

function Panel() {
  const [minStockProducts, setMinStockProducts] = useState([]);
  const [lowStockProducts, setLowStockProducts] = useState([]);

  // Definir los umbrales
  const MIN_THRESHOLD = 10; // Stock mínimo
  const LOW_THRESHOLD = 5;  // Por agotarse

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const response = await axios.get('http://localhost:5000/products');
        const products = response.data;

        // Filtrar productos según los umbrales
        const minStock = products.filter((product) => product.stock <= MIN_THRESHOLD && product.stock > LOW_THRESHOLD);
        const lowStock = products.filter((product) => product.stock <= LOW_THRESHOLD);

        setMinStockProducts(minStock);
        setLowStockProducts(lowStock);
      } catch (error) {
        console.error('Error al cargar los productos:', error);
      }
    };

    fetchProducts();
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
