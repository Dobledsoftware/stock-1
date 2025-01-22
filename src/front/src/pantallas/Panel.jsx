import React, { useEffect, useState } from 'react';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Typography, Grid } from '@mui/material';
import axios from 'axios';

function Panel() {
  const [minStockProducts, setMinStockProducts] = useState([]);
  const [lowStockProducts, setLowStockProducts] = useState([]);
  const [loading, setLoading] = useState(true);

  // Definir los umbrales
  const MIN_THRESHOLD = 10; // Stock mínimo
  const LOW_THRESHOLD = 5;  // Por agotarse

  // Llamada al endpoint para obtener los productos de stock
  useEffect(() => {
    const fetchStockData = async () => {
      try {
        const response = await axios.post(`${import.meta.env.VITE_API_BASE_URL}/tabla_stock`, {});
        console.log("Productos recibidos:", response.data); // Verifica la estructura de los datos
        const products = response.data || [];

        // Filtrar productos según los umbrales
        const minStock = products.filter((product) => 
          product.stock_actual != null && 
          product.stock_minimo != null && 
          product.stock_actual <= MIN_THRESHOLD && 
          product.stock_actual > LOW_THRESHOLD && 
          product.estado
        );
        const lowStock = products.filter((product) => 
          product.stock_actual != null && 
          product.stock_minimo != null && 
          product.stock_actual <= LOW_THRESHOLD && 
          product.estado
        );

        console.log("Productos en el mínimo:", minStock); // Verifica los productos filtrados
        console.log("Productos por agotarse:", lowStock); // Verifica los productos filtrados

        setMinStockProducts(minStock);
        setLowStockProducts(lowStock);
      } catch (error) {
        console.error("Error al obtener los productos de stock:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchStockData();
  }, []);

  if (loading) {
    return <Typography variant="h6" align="center">Cargando...</Typography>;
  }

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
                <TableCell>Stock Actual</TableCell>
                <TableCell>Stock Mínimo</TableCell>
                <TableCell>Stock Máximo</TableCell>
                <TableCell>Estado</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {minStockProducts.length > 0 ? (
                minStockProducts.map((product) => (
                  <TableRow key={product.id_stock}>
                    <TableCell>{product.id_producto}</TableCell> {/* Aquí podrías reemplazar por el nombre del producto si lo tienes */}
                    <TableCell>{product.stock_actual}</TableCell>
                    <TableCell>{product.stock_minimo}</TableCell>
                    <TableCell>{product.stock_maximo}</TableCell>
                    <TableCell>
                      {product.stock_actual < product.stock_minimo ? "Por debajo del mínimo" : "Suficiente"}
                    </TableCell>
                  </TableRow>
                ))
              ) : (
                <TableRow>
                  <TableCell colSpan={5} align="center">
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
                <TableCell>Stock Actual</TableCell>
                <TableCell>Stock Mínimo</TableCell>
                <TableCell>Stock Máximo</TableCell>
                <TableCell>Estado</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {lowStockProducts.length > 0 ? (
                lowStockProducts.map((product) => (
                  <TableRow key={product.id_stock}>
                    <TableCell>{product.id_producto}</TableCell> {/* Aquí podrías reemplazar por el nombre del producto si lo tienes */}
                    <TableCell>{product.stock_actual}</TableCell>
                    <TableCell>{product.stock_minimo}</TableCell>
                    <TableCell>{product.stock_maximo}</TableCell>
                    <TableCell>
                      {product.stock_actual < product.stock_minimo ? "Por debajo del mínimo" : "Suficiente"}
                    </TableCell>
                  </TableRow>
                ))
              ) : (
                <TableRow>
                  <TableCell colSpan={5} align="center">
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
