document.getElementById('generate-pdf').addEventListener('click', () => {
    // Verifica si jsPDF está disponible
    if (!window.jspdf || !window.jspdf.jsPDF) {
        console.error('jsPDF no está cargado. Verifica que la librería esté incluida correctamente.');
        return;
    }

    const { jsPDF } = window.jspdf;
    const pdf = new jsPDF();

    // Configuración inicial del PDF
    pdf.setFont("Arial", "normal");
    pdf.setFontSize(12);

    // Encabezado
    pdf.text("Planilla de Solicitud para Pacientes", 10, 10);
    pdf.text("Hospital Nacional Profesor Alejandro Posadas", 10, 20);

    // Campos de la primera página
    pdf.text("Fecha:", 10, 30);
    pdf.text("__________________________________", 50, 30);
    pdf.text("Nombre y Apellido:", 10, 40);
    pdf.text("__________________________________", 50, 40);

    pdf.text("DNI:", 10, 50);
    pdf.text("__________________________________", 50, 50);

    pdf.text("Fecha de Nacimiento:", 10, 60);
    pdf.text("__________________________________", 50, 60);

    pdf.text("Edad:", 10, 70);
    pdf.text("__________________________________", 50, 70);

    pdf.text("Teléfono:", 10, 80);
    pdf.text("__________________________________", 50, 80);

    pdf.text("Correo Electrónico:", 10, 90);
    pdf.text("__________________________________", 50, 90);

    pdf.text("Nº Historia Clínica:", 10, 100);
    pdf.text("__________________________________", 50, 100);

    pdf.text("Piso:", 10, 110);
    pdf.text("__________________________________", 50, 110);

    pdf.text("Cama:", 10, 120);
    pdf.text("__________________________________", 50, 120);

    pdf.text("Obra Social:", 10, 130);
    pdf.text("__________________________________", 50, 130);

    pdf.text("Diagnóstico:", 10, 140);
    pdf.text("__________________________________", 50, 140);

    pdf.text("Insumos/Estudios Solicitados:", 10, 150);
    pdf.text("__________________________________", 50, 150);

    // Crear campos de formulario interactivos
    pdf.text("Fecha: ", 10, 35);
    pdf.text("Fecha", 50, 35);
    pdf.formTextField(50, 35, 60, 10, { name: 'fecha', value: '', multiline: false });

    pdf.text("Nombre y Apellido:", 10, 45);
    pdf.formTextField(50, 45, 100, 10, { name: 'nombre', value: '', multiline: false });

    pdf.text("DNI:", 10, 55);
    pdf.formTextField(50, 55, 100, 10, { name: 'dni', value: '', multiline: false });

    pdf.text("Fecha de Nacimiento:", 10, 65);
    pdf.formTextField(50, 65, 100, 10, { name: 'fecha-nac', value: '', multiline: false });

    pdf.text("Edad:", 10, 75);
    pdf.formTextField(50, 75, 100, 10, { name: 'edad', value: '', multiline: false });

    pdf.text("Teléfono:", 10, 85);
    pdf.formTextField(50, 85, 100, 10, { name: 'telefono', value: '', multiline: false });

    pdf.text("Correo Electrónico:", 10, 95);
    pdf.formTextField(50, 95, 100, 10, { name: 'email', value: '', multiline: false });

    pdf.text("Nº Historia Clínica:", 10, 105);
    pdf.formTextField(50, 105, 100, 10, { name: 'hc', value: '', multiline: false });

    pdf.text("Piso:", 10, 115);
    pdf.formTextField(50, 115, 100, 10, { name: 'piso', value: '', multiline: false });

    pdf.text("Cama:", 10, 125);
    pdf.formTextField(50, 125, 100, 10, { name: 'cama', value: '', multiline: false });

    pdf.text("Obra Social:", 10, 135);
    pdf.formTextField(50, 135, 100, 10, { name: 'obra-social', value: '', multiline: false });

    pdf.text("Diagnóstico:", 10, 145);
    pdf.formTextField(50, 145, 100, 10, { name: 'diagnostico', value: '', multiline: false });

    pdf.text("Insumos/Estudios Solicitados:", 10, 155);
    pdf.formTextField(50, 155, 100, 10, { name: 'insumos', value: '', multiline: false });

    // Segunda página
    pdf.addPage();
    pdf.text("Resumen de Historia Clínica y Observaciones", 10, 10);

    pdf.text("Resumen de Historia Clínica:", 10, 20);
    pdf.formTextField(50, 20, 100, 10, { name: 'resumen-hc', value: '', multiline: true });

    pdf.text("Observaciones:", 10, 40);
    pdf.formTextField(50, 40, 100, 10, { name: 'observaciones', value: '', multiline: true });

    // Descargar PDF
    pdf.save("Planilla_Pacientes_Editable.pdf");
});