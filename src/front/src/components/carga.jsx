import '../styles/carga.css'; // Asegúrate de tener estilos para tu componente
import { useState } from 'react';
import { useSnackbar } from 'notistack';
import LinearProgress from '@mui/material/LinearProgress';

const Carga = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [fileName, setFileName] = useState(''); // Estado para el nombre del archivo
  const [isLoading, setIsLoading] = useState(false);
  const [validationData, setValidationData] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [isProcessed, setIsProcessed] = useState(false);
  const { enqueueSnackbar } = useSnackbar();

  // Manejar la selección del archivo
  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      setSelectedFile(file);
      setFileName(file.name); // Actualiza el estado con el nombre del archivo
      enqueueSnackbar('Archivo seleccionado: ' + file.name, { variant: 'success' });
    } else {
      setFileName(''); // Resetea el nombre si no hay archivo
      enqueueSnackbar('No se seleccionó ningún archivo', { variant: 'error' });
    }
  };

  const handleValidate = async (event) => {
    event.preventDefault();
    if (!selectedFile) {
      enqueueSnackbar('Por favor, selecciona un archivo antes de enviar.', { variant: 'error' });
      return;
    }

    setIsLoading(true);
    const formData = new FormData();
    formData.append('file', selectedFile);
    formData.append('action', 'validar');

    try {
      const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/upload`, {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        setValidationData(data);
        enqueueSnackbar('Archivo validado exitosamente!', { variant: 'success' });
      } else {
        enqueueSnackbar('Error al validar el archivo.', { variant: 'error' });
      }
    } catch (error) {
      console.error('Error en la validación del archivo:', error);
      enqueueSnackbar('Error en la validación del archivo.', { variant: 'error' });
    } finally {
      setIsLoading(false);
    }
  };

  const handleProcess = async () => {
    if (!validationData) {
      enqueueSnackbar('No hay datos válidos para procesar.', { variant: 'error' });
      return;
    }

    setIsProcessing(true);
    const formData = new FormData();
    formData.append('file', selectedFile);
    formData.append('action', 'procesar');

    try {
      const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/upload`, {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        enqueueSnackbar('Archivo procesado exitosamente!', { variant: 'success' });
        setIsProcessed(true);
      } else {
        enqueueSnackbar('Error al procesar el archivo.', { variant: 'error' });
      }
    } catch (error) {
      console.error('Error en el procesamiento del archivo:', error);
      enqueueSnackbar('Error en el procesamiento del archivo.', { variant: 'error' });
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="carga-container">
      {/* Logo de la aplicación */}
      <div className="logo-container">
                <img src="/public/img/LOGO_POSADAS_sin_fondo_COLOR_HORIZONTAL.png" alt="Logo2" className="logo2"/>
            </div>
      <h2>Cargador de Recibos</h2>
      {!validationData && !isProcessed ? (
        <form onSubmit={handleValidate} className="form-container">
          <label htmlFor="file-upload" className="upload-button">
            Seleccionar archivo
          </label>
          <input
            type="file"
            id="file-upload"
            onChange={handleFileChange}
            style={{ display: 'none' }} // Oculta el input
          />
          <div className="file-info">
            {fileName && <p className="file-name">Archivo seleccionado: {fileName}</p>}
            <button type="submit" className="upload-button" disabled={isLoading}>
              Enviar
            </button>
          </div>
        </form>
      ) : null}

      {isLoading && <LinearProgress />}

      {validationData && !isProcessed && (
        <div className="validation-data">
          <h3>Datos de Validación</h3>
          <table>
            <thead>
              <tr>
                <th>Campo</th>
                <th>Valor</th>
              </tr>
            </thead>
            <tbody>
              {Object.entries(validationData).map(([key, value]) => (
                <tr key={key}>
                  <td>{key}</td>
                  <td>{value}</td>
                </tr>
              ))}
            </tbody>
          </table>
          <button
            className="process-button"
            onClick={handleProcess}
            disabled={isProcessing}
          >
            Procesar
          </button>
        </div>
      )}

      {isProcessing && <LinearProgress />}

      {isProcessed && (
        <div className="success-message">
          <h3>¡Proceso completado exitosamente!</h3>
        </div>
      )}
    </div>
  );
};

export default Carga;
