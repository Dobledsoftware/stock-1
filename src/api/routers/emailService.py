import smtplib
import ssl
from email.message import EmailMessage
import random
import string

class EmailService:
    def __init__(self, remitente, password):
        self.remitente = remitente
        self.password = password
        self.context = ssl.create_default_context()

    def generar_contrasena_provisoria(self, length=8):
        """Generar una contraseña aleatoria de longitud especificada."""
        caracteres = string.ascii_letters + string.digits
        return ''.join(random.choice(caracteres) for i in range(length))

    def enviar_correo(self, destinatario, asunto, cuerpo):
        print("entro a enviar correo")
        """Enviar un correo electrónico."""
        mensaje = EmailMessage()
        mensaje['Subject'] = asunto
        mensaje['From'] = self.remitente
        mensaje['To'] = destinatario
        mensaje.set_content(cuerpo)

        try:
            with smtplib.SMTP_SSL('mail.hospitalposadas.gob.ar', 465, context=self.context) as servidor:
                servidor.login(self.remitente, self.password)
                servidor.send_message(mensaje)
                print(f"Correo enviado exitosamente a {destinatario}")
        except Exception as e:
            print(f"Error al enviar el correo: {e}")
