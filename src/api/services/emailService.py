import os
import smtplib
from email.message import EmailMessage

class EmailService:
    """
    Servicio para enviar correos electrónicos mediante SMTP.
    """

    def __init__(self):
        """Inicializa la configuración del servidor SMTP desde las variables de entorno."""
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", 465))  # 465 (SSL) o 587 (TLS)
        self.smtp_user = os.getenv("SMTP_USER")
        self.smtp_password = os.getenv("SMTP_PASSWORD")

        if not self.smtp_user or not self.smtp_password:
            print("⚠️ ERROR: Credenciales SMTP no configuradas.")

    def send_email(self, to: str, subject: str, body: str):
        """
        Envía un correo electrónico usando SMTP.

        Parámetros:
        - `to` (str): Dirección de correo del destinatario.
        - `subject` (str): Asunto del correo.
        - `body` (str): Cuerpo del correo en texto plano.
        """
        if not self.smtp_user or not self.smtp_password:
            print("❌ ERROR: No se pueden enviar correos sin credenciales SMTP.")
            return False

        msg = EmailMessage()
        msg["From"] = self.smtp_user
        msg["To"] = to
        msg["Subject"] = subject
        msg.set_content(body)

        try:
            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as server:
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
            print(f"📧 Correo enviado a {to} con asunto '{subject}'")
            return True
        except Exception as e:
            print(f"❌ ERROR al enviar correo: {e}")
            return False
