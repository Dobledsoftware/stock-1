import React, { useState } from 'react';
import '../styles/cierreCaja.css';

const CierreCaja = () => {
    const [fecha, setFecha] = useState(new Date().toISOString().split('T')[0]); // Fecha del cierre
    const [saldoInicial, setSaldoInicial] = useState(0); // Saldo inicial
    const [transacciones, setTransacciones] = useState([]); // Lista de transacciones
    const [motivo, setMotivo] = useState('');
    const [monto, setMonto] = useState(0);
    const [tipo, setTipo] = useState('ingreso'); // Tipo de transacción: ingreso o egreso

    // Calcular totales
    const totalIngresos = transacciones
        .filter((t) => t.tipo === 'ingreso')
        .reduce((sum, t) => sum + t.monto, 0);
    const totalEgresos = transacciones
        .filter((t) => t.tipo === 'egreso')
        .reduce((sum, t) => sum + t.monto, 0);
    const saldoFinal = saldoInicial + totalIngresos - totalEgresos;

    // Agregar una nueva transacción
    const agregarTransaccion = () => {
        if (!motivo.trim() || monto <= 0) {
            alert('Por favor, ingresa un motivo y un monto válido.');
            return;
        }

        const nuevaTransaccion = { motivo, monto, tipo };
        setTransacciones([...transacciones, nuevaTransaccion]);
        setMotivo('');
        setMonto(0);
    };

    // Confirmar el cierre de caja
    const confirmarCierre = () => {
        const balance = {
            fecha,
            saldoInicial,
            totalIngresos,
            totalEgresos,
            saldoFinal,
            transacciones,
        };

        console.log('Datos del cierre de caja enviados:', balance);
        alert('Cierre de caja confirmado.');
        // Resetear el formulario
        setSaldoInicial(0);
        setTransacciones([]);
    };

    return (
        <div className="cierre-caja">
            <h1>Cierre de Caja</h1>

            {/* Fecha del cierre */}
            <div className="form-control">
                <label>Fecha:</label>
                <input
                    type="date"
                    value={fecha}
                    onChange={(e) => setFecha(e.target.value)}
                />
            </div>

            {/* Saldo inicial */}
            <div className="form-control">
                <label>Saldo Inicial:</label>
                <input
                    type="number"
                    value={saldoInicial}
                    onChange={(e) => setSaldoInicial(parseFloat(e.target.value) || 0)}
                />
            </div>

            {/* Formulario para agregar transacciones */}
            <div className="form-transacciones">
                <h2>Registrar Transacción</h2>
                <select value={tipo} onChange={(e) => setTipo(e.target.value)}>
                    <option value="ingreso">Ingreso</option>
                    <option value="egreso">Egreso</option>
                </select>
                <input
                    type="text"
                    placeholder="Motivo"
                    value={motivo}
                    onChange={(e) => setMotivo(e.target.value)}
                />
                <input
                    type="number"
                    placeholder="Monto"
                    value={monto}
                    onChange={(e) => setMonto(parseFloat(e.target.value) || 0)}
                />
                <button onClick={agregarTransaccion}>Agregar</button>
            </div>

            {/* Tabla de transacciones */}
            <div className="tabla-transacciones">
                <h2>Transacciones</h2>
                {transacciones.length > 0 ? (
                    <table>
                        <thead>
                            <tr>
                                <th>Motivo</th>
                                <th>Tipo</th>
                                <th>Monto</th>
                            </tr>
                        </thead>
                        <tbody>
                            {transacciones.map((t, index) => (
                                <tr key={index}>
                                    <td>{t.motivo}</td>
                                    <td>{t.tipo === 'ingreso' ? 'Ingreso' : 'Egreso'}</td>
                                    <td>${t.monto.toFixed(2)}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                ) : (
                    <p>No hay transacciones registradas.</p>
                )}
            </div>

            {/* Balance final */}
            <div className="balance">
                <h2>Balance</h2>
                <p>Total Ingresos: ${totalIngresos.toFixed(2)}</p>
                <p>Total Egresos: ${totalEgresos.toFixed(2)}</p>
                <p>Saldo Final: ${saldoFinal.toFixed(2)}</p>
            </div>

            {/* Botón de confirmación */}
            <button onClick={confirmarCierre} className="btn-confirmar">
                Confirmar Cierre de Caja
            </button>
        </div>
    );
};

export default CierreCaja;
